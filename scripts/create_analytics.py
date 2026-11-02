from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_FILE = ROOT / "database" / "students.db"
COLUMNS = ["school", "age", "absences", "G1", "G2", "G3", "average_marks", "risk_level"]

def main():
    if not DB_FILE.exists():
        raise FileNotFoundError("SQLite database not found. Run scripts/load_database.py first.")
    with sqlite3.connect(DB_FILE) as conn:
        available = {row[1] for row in conn.execute("PRAGMA table_info(students)")}
        missing = set(COLUMNS).difference(available)
        if missing:
            raise ValueError(f"students table is missing columns: {sorted(missing)}")
        df = pd.read_sql_query(f"SELECT {', '.join(COLUMNS)} FROM students", conn)
        df.to_sql("student_performance_summary", conn, if_exists="replace", index=False)
        count = conn.execute("SELECT COUNT(*) FROM student_performance_summary").fetchone()[0]
    print(f"Created student_performance_summary with {count} records.")

if __name__ == "__main__":
    main()
