from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "cleaned" / "student_cleaned.csv"
DB_DIR = ROOT / "database"
DB_FILE = DB_DIR / "students.db"

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Cleaned data not found. Run scripts/pipeline.py first.")
    DB_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_FILE)
    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql("students", conn, if_exists="replace", index=False)
        count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    print(f"Loaded {count} records into {DB_FILE.relative_to(ROOT)} (table: students).")

if __name__ == "__main__":
    main()
