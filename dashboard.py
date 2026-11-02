from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
DB_FILE = ROOT / "database" / "students.db"

st.set_page_config(page_title="Student Performance Dashboard", page_icon="🎓", layout="wide")
st.title("🎓 Student Performance & Academic Risk Dashboard")
st.caption("Academic-risk indicators are rule-derived and are not verified dropout outcomes.")

@st.cache_data
def load_students(db_path, modified_time):
    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query("SELECT * FROM students", connection)

if not DB_FILE.exists():
    st.error("Database not found. Run `python scripts/pipeline.py` from the project root first.")
    st.stop()

try:
    df = load_students(str(DB_FILE), DB_FILE.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not read the SQLite database: {exc}")
    st.stop()

if df.empty:
    st.warning("The students table is empty. Run the ETL pipeline.")
    st.stop()

required = {"average_marks", "risk_level", "absences", "G3", "age", "school"}
missing = required.difference(df.columns)
if missing:
    st.error(f"Database table is missing columns: {sorted(missing)}")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Students", len(df))
c2.metric("Average Marks", f"{df['average_marks'].mean():.2f}")
c3.metric("High Academic Risk", int((df["risk_level"] == "High").sum()))
c4.metric("Average Absences", f"{df['absences'].mean():.1f}")

st.subheader("Academic Risk Distribution")
risk_order = ["High", "Medium", "Low"]
risk_counts = df["risk_level"].value_counts().reindex(risk_order, fill_value=0).rename_axis("Risk Level").reset_index(name="Students")
st.plotly_chart(px.bar(risk_counts, x="Risk Level", y="Students", color="Risk Level", text="Students"), use_container_width=True)

risk_filter = st.selectbox("Filter by risk category", ["All Students"] + risk_order)
view = df if risk_filter == "All Students" else df[df["risk_level"] == risk_filter]
st.caption(f"Showing {len(view)} of {len(df)} records.")

left, right = st.columns(2)
with left:
    st.subheader("Absences vs Final Grade")
    st.plotly_chart(px.scatter(view, x="absences", y="G3", color="risk_level", labels={"G3": "Final grade"}), use_container_width=True)
with right:
    st.subheader("Average Marks by Risk")
    avg_risk = view.groupby("risk_level", as_index=False)["average_marks"].mean()
    st.plotly_chart(px.bar(avg_risk, x="risk_level", y="average_marks", color="risk_level"), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Final Grade by Age")
    age_avg = view.groupby("age", as_index=False)["G3"].mean()
    st.plotly_chart(px.bar(age_avg, x="age", y="G3", labels={"G3": "Average final grade"}), use_container_width=True)
with right:
    st.subheader("Final Grade by School")
    school_avg = view.groupby("school", as_index=False)["G3"].mean()
    st.plotly_chart(px.bar(school_avg, x="school", y="G3", color="school"), use_container_width=True)

st.subheader("Student Academic Risk Details")
display_cols = [c for c in ["school", "sex", "age", "absences", "G1", "G2", "G3", "average_marks", "risk_level"] if c in view.columns]
st.dataframe(view[display_cols].sort_values("average_marks"), use_container_width=True, hide_index=True)
