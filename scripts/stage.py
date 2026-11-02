"""Copy ingested raw data into the staging area."""
import shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "student_raw.csv"
STAGING = ROOT / "data" / "staging" / "student_staging.csv"
def main():
    if not RAW.exists():
        raise FileNotFoundError("Raw data missing. Run scripts/ingest.py first.")
    STAGING.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(RAW, STAGING)
    print(f"Staging copy created: {STAGING.relative_to(ROOT)}")
if __name__ == "__main__":
    main()
