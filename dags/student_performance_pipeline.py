"""Airflow DAG that runs the repository ETL in dependency order."""
from datetime import datetime
from pathlib import Path
import subprocess
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_ROOT = Path("/opt/airflow/project") if Path("/opt/airflow/project").exists() else Path(__file__).resolve().parents[1]
PYTHON = sys.executable

def run_script(relative_path: str):
    subprocess.run([PYTHON, str(PROJECT_ROOT / relative_path)], cwd=str(PROJECT_ROOT), check=True)

with DAG(
    dag_id="student_performance_etl",
    description="Ingest, stage, clean, load PostgreSQL and create analytics",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["student-performance", "etl"],
) as dag:
    ingest = PythonOperator(task_id="ingest_csv", python_callable=run_script, op_kwargs={"relative_path": "scripts/ingest.py"})
    stage = PythonOperator(task_id="stage_csv", python_callable=run_script, op_kwargs={"relative_path": "scripts/stage.py"})
    clean = PythonOperator(task_id="clean_validate", python_callable=run_script, op_kwargs={"relative_path": "scripts/clean.py"})
    load = PythonOperator(task_id="load_postgresql", python_callable=run_script, op_kwargs={"relative_path": "scripts/load_database.py"})
    analytics = PythonOperator(task_id="create_analytics", python_callable=run_script, op_kwargs={"relative_path": "scripts/create_analytics.py"})
    ingest >> stage >> clean >> load >> analytics
