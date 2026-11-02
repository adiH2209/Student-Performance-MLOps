from sqlalchemy import text
from db import get_engine

COLUMNS = ["school", "age", "absences", "G1", "G2", "G3", "average_marks", "risk_level"]

def main():
    engine = get_engine()
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'students'")).scalars().all()
        missing = set(COLUMNS).difference(rows)
        if missing:
            raise ValueError(f"students table is missing columns: {sorted(missing)}")
        conn.execute(text("DROP TABLE IF EXISTS student_performance_summary"))
        conn.execute(text("CREATE TABLE student_performance_summary AS SELECT school, age, absences, \"G1\", \"G2\", \"G3\", average_marks, risk_level FROM students"))
        count = conn.execute(text("SELECT COUNT(*) FROM student_performance_summary")).scalar_one()
    print(f"Created PostgreSQL student_performance_summary with {count} records.")

if __name__ == "__main__":
    main()
