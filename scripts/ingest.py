import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "student-mat.csv"
RAW_DIR = ROOT / "data" / "raw"
RAW_FILE = RAW_DIR / "student_raw.csv"

def main():
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {SOURCE}\n"
            "Download the UCI Student Performance dataset and place student-mat.csv in data/."
        )
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(SOURCE, sep=";")
    df.to_csv(RAW_FILE, index=False)
    print("=" * 48)
    print("STUDENT DATA INGESTION")
    print("=" * 48)
    print("Timestamp:", datetime.now().isoformat(timespec="seconds"))
    print("Source:", SOURCE.relative_to(ROOT))
    print("Rows:", len(df), "| Columns:", len(df.columns))
    print("Raw copy:", RAW_FILE.relative_to(ROOT))

if __name__ == "__main__":
    main()
