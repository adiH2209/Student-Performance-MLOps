import subprocess
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_FILE = DATA_DIR / "raw" / "student_raw.csv"
STAGING_FILE = DATA_DIR / "staging" / "student_staging.csv"

def run(script):
    print(f"\n>>> Running {script}", flush=True)
    subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)

def main():
    print("=" * 52)
    print("STUDENT PERFORMANCE ETL PIPELINE")
    print("=" * 52)
    run("scripts/ingest.py")
    STAGING_FILE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(RAW_FILE, STAGING_FILE)
    print(f"Staging copy created: {STAGING_FILE.relative_to(ROOT)}")
    run("scripts/clean.py")
    run("scripts/load_database.py")
    run("scripts/create_analytics.py")
    print("\nETL pipeline completed successfully.")

if __name__ == "__main__":
    main()
