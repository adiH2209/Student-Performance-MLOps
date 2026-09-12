import subprocess
import shutil
import os

print("================================")
print("STUDENT PERFORMANCE ETL PIPELINE")
print("================================")

project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# 1. Data ingestion
print("\n1. Starting data ingestion...")
subprocess.run(["python", "scripts/ingest.py"], check=True)

# 2. Staging
print("\n2. Creating staging layer...")
staging_folder = os.path.join(project_folder, "data", "staging")
cleaned_file = os.path.join(
    project_folder, "data", "cleaned", "student_cleaned.csv"
)
staging_file = os.path.join(
    staging_folder, "student_cleaned.csv"
)

os.makedirs(staging_folder, exist_ok=True)
shutil.copy2(cleaned_file, staging_file)

print("Staging file created successfully.")

# 3. Data cleaning
print("\n3. Starting data cleaning...")
subprocess.run(["python", "scripts/clean.py"], check=True)

# 4. Database loading
print("\n4. Loading data into database...")
subprocess.run(["python", "scripts/load_database.py"], check=True)

# 5. Analytical table
print("\n5. Creating analytical table...")
subprocess.run(["python", "scripts/create_analytics.py"], check=True)

print("\n================================")
print("ETL PIPELINE COMPLETED SUCCESSFULLY")
print("================================")