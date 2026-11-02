"""Run the ETL pipeline locally; Airflow DAG is available in dags/."""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def main():
    for script in ["scripts/ingest.py", "scripts/stage.py", "scripts/clean.py", "scripts/load_database.py", "scripts/create_analytics.py"]:
        print(f"\n>>> Running {script}", flush=True)
        subprocess.run([sys.executable, str(ROOT / script)], cwd=ROOT, check=True)
    print("\nETL pipeline completed successfully.")
if __name__ == "__main__":
    main()
