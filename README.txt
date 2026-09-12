STUDENT PERFORMANCE AND DROPOUT-RISK PREDICTION SYSTEM

1. PROJECT DESCRIPTION

This project analyzes student academic performance and identifies
students who may require academic attention.

The project uses the UCI Student Performance Dataset and processes
the data through an automated ETL pipeline.

2. TECHNOLOGIES USED

- Python
- Pandas
- SQLite
- Streamlit

3. PROJECT STRUCTURE

Student_Performance_MLOps/
│
├── data/
│   ├── raw/
│   ├── staging/
│   ├── cleaned/
│   └── errors/
│
├── database/
│   └── students.db
│
├── scripts/
│   ├── ingest.py
│   ├── clean.py
│   ├── load_database.py
│   ├── create_analytics.py
│   └── pipeline.py
│
├── dashboard.py
├── data_dictionary.txt
├── dataset_source.txt
└── README.txt

4. HOW TO RUN THE PROJECT

Step 1:
Open a terminal in the project folder.

Step 2:
Run the complete ETL pipeline:

python scripts\pipeline.py

Step 3:
Start the Streamlit dashboard:

python -m streamlit run dashboard.py

Step 4:
Open the Streamlit dashboard in the browser.

5. ETL PIPELINE

The pipeline performs the following operations:

UCI Dataset
    ↓
Data Ingestion
    ↓
Raw Data
    ↓
Staging
    ↓
Cleaning and Validation
    ↓
Error Log
    ↓
Cleaned Data
    ↓
SQLite Database
    ↓
Analytical Table
    ↓
Streamlit Dashboard

6. DATA QUALITY CHECKS

The project checks for:

- Missing values
- Duplicate records
- Invalid marks
- Valid mark range from 0 to 20

Rejected records are stored in:

data/errors/rejected_records.csv

7. DASHBOARD

The Streamlit dashboard displays:

- Total students
- Average marks
- High-risk students
- Average absences
- Academic risk distribution
- Absences versus final marks
- Student risk details
- Risk-level filtering

8. NOTE

The risk_level is an academic-risk indicator and is not a confirmed
dropout prediction.

The selected UCI dataset does not contain actual attendance percentage
or assignment-completion data. The available absences field is used
as an academic-risk indicator.