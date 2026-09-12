import pandas as pd
import os
from datetime import datetime

# File locations
input_file = "data/student-mat.csv"
raw_folder = "data/raw"

# Create raw data folder
os.makedirs(raw_folder, exist_ok=True)

# Read the dataset
df = pd.read_csv(input_file, sep=";")

# Save a raw copy
raw_file = os.path.join(raw_folder, "student_raw.csv")
df.to_csv(raw_file, index=False)

# Ingestion information
print("================================")
print("STUDENT DATA INGESTION")
print("================================")
print("Extraction date:", datetime.now())
print("Source file:", input_file)
print("Status: SUCCESS")
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))
print("Raw copy saved to:", raw_file)

print("\nFirst 5 records:")
print(df.head())