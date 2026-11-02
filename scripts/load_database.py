from pathlib import Path
import pandas as pd
from db import get_engine

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "cleaned" / "student_cleaned.csv"

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Cleaned data not found. Run scripts/pipeline.py first.")
    df = pd.read_csv(INPUT_FILE)
    with get_engine().begin() as conn:
        df.to_sql("students", conn, if_exists="replace", index=False, method="multi", chunksize=500)
    print(f"Loaded {len(df)} records into PostgreSQL table students.")

if __name__ == "__main__":
    main()
