import psycopg2
import streamlit as st
import pandas as pd
import os
import plotly.express as px
# Project folder
project_folder = os.path.dirname(os.path.abspath(__file__))

# Database location
database_file = os.path.join(
    project_folder,
    "database",
    "students.db"
)

# Connect to database
connection = psycopg2.connect(
    host="172.31.112.1",
    database="student_performance",
    user="postgres",
    password="aditya@22",
    port=5432
)

# Read student data
df = pd.read_sql_query(
    "SELECT * FROM students",
    connection
)

connection.close()

# Page settings
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Title
st.title("🎓 Student Performance & Academic Risk Dashboard")

st.write(
    "This dashboard analyzes student academic performance "
    "and identifies students who may require academic attention."
)

# Key calculations
total_students = len(df)
average_marks = df["average_marks"].mean()
high_risk = len(df[df["risk_level"] == "High"])
average_absences = df["absences"].mean()

# Dashboard numbers
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", total_students)
col2.metric("Average Marks", round(average_marks, 2))
col3.metric("High Risk Students", high_risk)
col4.metric("Average Absences", round(average_absences, 1))

# Risk distribution
# Risk distribution
st.subheader("📊 Academic Risk Distribution")

risk_counts = (
    df["risk_level"]
    .value_counts()
    .reindex(["High", "Medium", "Low"])
    .reset_index()
)

risk_counts.columns = ["risk_level", "count"]

fig1 = px.bar(
    risk_counts,
    x="risk_level",
    y="count",
    color="risk_level",
    color_discrete_map={
        "High": "#E74C3C",
        "Medium": "#F39C12",
        "Low": "#2ECC71"
    },
    text="count",
    labels={
        "risk_level": "Risk Level",
        "count": "Number of Students"
    }
)

fig1.update_traces(
    textposition="outside",
    marker_line_width=1.5
)

fig1.update_layout(
    title="Students by Academic Risk Level",
    title_x=0.5,
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(
        title="Number of Students",
        gridcolor="rgba(128,128,128,0.2)"
    ),
    xaxis=dict(
        title="Risk Level"
    ),
    margin=dict(t=70, l=40, r=40, b=40)
)

st.plotly_chart(fig1, use_container_width=True)
# Risk filter
st.subheader("🔎 Filter Students by Risk")

risk_option = st.selectbox(
    "Select Risk Level",
    ["All Students", "High", "Medium", "Low"]
)

if risk_option == "All Students":
    filtered_df = df
else:
    filtered_df = df[df["risk_level"] == risk_option]

st.write("Students shown:", len(filtered_df))

# Absences vs marks
st.subheader("📈 Absences vs Final Marks")

chart_data = df[["absences", "g3"]].copy()

chart_data = chart_data.rename(
    columns={"g3": "Final Marks"}
)

st.scatter_chart(
    chart_data,
    x="absences",
    y="Final Marks"
)

# Student table
st.subheader("⚠️ Student Risk Details")
# Graph 3 - Average Marks by Risk Level
st.subheader("📊 Average Marks by Risk Level")

risk_avg = (
    filtered_df.groupby("risk_level")["average_marks"]
    .mean()
    .reset_index()
)

fig3 = px.bar(
    risk_avg,
    x="risk_level",
    y="average_marks",
    color="risk_level",
    color_discrete_map={
        "High": "#E74C3C",
        "Medium": "#F39C12",
        "Low": "#2ECC71"
    },
    labels={
        "risk_level": "Risk Level",
        "average_marks": "Average Marks"
    }
)

st.plotly_chart(fig3, use_container_width=True)


# Graph 4 - Average Marks by Study Time
# Graph 4 - Average Marks by Age
st.subheader("👥 Average Marks by Age")

age_avg = (
    filtered_df.groupby("age")["g3"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    age_avg,
    x="age",
    y="g3",
    color="age",
    labels={
        "age": "Age",
        "g3": "Average Final Marks"
    }
)

st.plotly_chart(fig4, use_container_width=True)
# Graph 5 - Average Marks by School
st.subheader("🏫 Average Marks by School")

school_avg = (
    filtered_df.groupby("school")["g3"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    school_avg,
    x="school",
    y="g3",
    color="school",
    labels={
        "school": "School",
        "g3": "Average Final Marks"
    }
)

st.plotly_chart(fig5, use_container_width=True)

risk_students = filtered_df[
    [
        "school",
        "sex",
        "age",
        "absences",
        "g1",
        "g2",
        "g3",
        "average_marks",
        "risk_level"
    ]
]

risk_students = risk_students.sort_values(
    by="average_marks"
)

st.dataframe(
    risk_students,
    use_container_width=True
)

# Note
st.info(
    "Risk level is calculated using final marks and absences. "
    "It is an academic-risk indicator and not a confirmed dropout prediction."
)
