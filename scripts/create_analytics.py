import pandas as pd
import sqlite3
import os

# Find project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Database path
database_file = os.path.join(
    project_folder,
    "database",
    "students.db"
)

# Connect to database
connection = sqlite3.connect(database_file)

# Read required data
df = pd.read_sql_query(
    """
    SELECT
        school,
        age,
        absences,
        G1,
        G2,
        G3,
        average_marks,
        risk_level
    FROM students
    """,
    connection
)

# Create analytical table
df.to_sql(
    "student_performance_summary",
    connection,
    if_exists="replace",
    index=False
)

# Check table
cursor = connection.cursor()
cursor.execute(
    "SELECT COUNT(*) FROM student_performance_summary"
)

count = cursor.fetchone()[0]

connection.close()

print("================================")
print("ANALYTICAL TABLE CREATION")
print("================================")
print("Table: student_performance_summary")
print("Records:", count)
print("Status: SUCCESS")