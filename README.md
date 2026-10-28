# 🎓 Student Performance and Dropout-Risk Prediction System

An end-to-end Data Engineering and MLOps project that analyzes student performance and classifies students into academic-risk categories using machine learning.

## 🚀 Project Overview

This project combines automated data processing, machine learning, experiment tracking, API deployment, and monitoring in one workflow.

## 🛠️ Technology Stack

- **Programming:** Python
- **Data Processing:** Pandas
- **Database:** PostgreSQL
- **Data Pipeline:** Apache Airflow
- **Machine Learning:** Scikit-learn, XGBoost
- **Experiment Tracking:** MLflow
- **Dataset Versioning:** DVC
- **Dashboard:** Streamlit
- **API:** FastAPI
- **Containerization:** Docker
- **Version Control:** Git and GitHub

## 📊 Key Features

- Automated data ingestion and cleaning
- Data quality checks and analytical reporting
- Interactive student performance dashboard
- Logistic Regression, Random Forest, and XGBoost model comparison
- MLflow experiment tracking and model registration
- Dataset versioning using DVC
- Academic-risk predictions through FastAPI
- Docker-based API deployment
- Prediction monitoring and retraining scripts

## 🧠 Model Performance

| Model | Accuracy |
|---|---:|
| Logistic Regression | 78.48% |
| Random Forest | 86.08% |
| XGBoost | 87.34% |

*Results from the current model comparison; performance may vary with data and evaluation settings.*

## 📁 Project Structure

```text
Student_Performance_MLOps/
├── data/
│   ├── raw/
│   ├── staging/
│   └── cleaned/
├── database/
├── ml/
│   ├── model/
│   ├── compare_models.py
│   ├── retrain.py
│   └── train_mlflow.py
├── monitoring/
│   └── monitor.py
├── scripts/
│   ├── ingest.py
│   ├── clean.py
│   └── pipeline.py
├── api.py
├── dashboard.py
├── Dockerfile
├── data_dictionary.txt
├── dataset_source.txt
└── README.md
```

## ▶️ Getting Started

1. Clone the repository.
2. Install the Python dependencies required by the project.
3. Configure PostgreSQL credentials using environment variables.
4. Start the Streamlit dashboard.
5. Start the FastAPI service to test predictions.
6. Start MLflow to inspect model experiments.

## ⚠️ Important Note

The current model predicts rule-derived academic-risk categories (High, Medium, and Low). These labels are not confirmed student-dropout outcomes, so the model should not be considered a validated dropout prediction system.

## 👨‍💻 Author

Aditya Harikumar

Student Performance and MLOps Project
