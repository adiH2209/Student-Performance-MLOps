import pandas as pd
import sqlite3
import os

# Find the main project folder
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File locations
input_file = os.path.join(
    project_folder,
    "data",
    "cleaned",
    "student_cleaned.csv"
)

database_folder = os.path.join(project_folder, "database")

# Create database folder
os.makedirs(database_folder, exist_ok=True)

# Database file
database_file = os.path.join(database_folder, "students.db")

# Read cleaned data
df = pd.read_csv(input_file)

# Connect to SQLite database
connection = sqlite3.connect(database_file)

# Load data into database
df.to_sql("students", connection, if_exists="replace", index=False)

# Check number of records
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM students")
count = cursor.fetchone()[0]

connection.close()

print("================================")
print("DATABASE LOADING")
print("================================")
print("Database:", database_file)
print("Table: students")
print("Records loaded:", count)
print("Status: SUCCESS")