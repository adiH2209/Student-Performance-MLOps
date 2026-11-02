# Student Performance & Academic-Risk Classification

A Python-based data and machine-learning project that processes the UCI Student Performance Mathematics dataset, derives academic-risk categories, compares classification models, tracks experiments with MLflow, serves predictions through FastAPI, and displays analysis in Streamlit.

> **Target definition:** `risk_level` is derived from final grade (`G3`) and absences using project-defined thresholds. The UCI dataset does not provide a verified future dropout outcome. This repository therefore demonstrates **academic-risk classification**, not a validated student-dropout prediction system.

## What the repository currently implements

- CSV ingestion and a repeatable Python ETL runner.
- Data validation, duplicate removal and rejected-record output.
- Derived `average_marks` and rule-based `risk_level`.
- SQLite storage and an analytical summary table.
- Logistic Regression, Random Forest and XGBoost comparison.
- MLflow logging for model parameters and evaluation metrics.
- A saved XGBoost model bundle that includes its label encoder and feature list.
- FastAPI endpoints for health checks and predictions.
- A Streamlit dashboard backed by the same SQLite database used by the ETL scripts.
- Prediction logging and basic feature-distribution monitoring.
- DVC pointer files for the source dataset and model artifact.
- A Dockerfile for the FastAPI service.

## Architecture

```text
UCI student-mat.csv
       |
       v
scripts/ingest.py
       |
       v
data/raw/student_raw.csv
       |
       v
data/staging/student_staging.csv
       |
       v
scripts/clean.py ------> data/errors/rejected_records.csv
       |
       v
data/cleaned/student_cleaned.csv
       |
       +--------------------------+
       |                          |
       v                          v
SQLite database              ML model comparison
database/students.db         Logistic Regression
       |                      Random Forest
       v                      XGBoost
student_performance_summary       |
                                  v
                            MLflow tracking
                                  |
                                  v
                       saved model + label encoder
                                  |
                                  v
                            FastAPI /predict
                                  |
                                  v
                      monitoring/predictions.csv
                                  |
                                  v
                           monitor.py

Streamlit dashboard ---> database/students.db
```

## Technology stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn, XGBoost |
| Experiment tracking | MLflow |
| Database | SQLite |
| Dashboard | Streamlit, Plotly |
| API | FastAPI, Uvicorn, Pydantic |
| Monitoring | Pandas, SciPy |
| Data/model versioning | DVC |
| Containerization | Docker |
| Version control | Git, GitHub |

**Orchestration note:** `scripts/pipeline.py` runs the ETL steps using Python's `subprocess` module. There is no Apache Airflow DAG in this repository snapshot, so Airflow is not listed as an implemented component.

## Repository structure

```text
Student-Performance-MLOps/
├── .dvc/                       # DVC configuration metadata
├── data/
│   ├── student-mat.csv.dvc     # DVC pointer for source dataset
│   ├── raw/                    # Generated raw CSV (ignored by Git)
│   ├── staging/                # Generated staging CSV (ignored by Git)
│   ├── cleaned/
│   │   └── student_cleaned.csv # Processed dataset
│   └── errors/                 # Rejected records (ignored by Git)
├── database/
│   └── students.db             # Generated SQLite database (ignored by Git)
├── ml/
│   ├── model/
│   │   └── student_risk_model.pkl.dvc
│   ├── model_utils.py
│   ├── compare_models.py
│   ├── train_model.py
│   ├── train_mlflow.py
│   └── retrain.py
├── monitoring/
│   └── monitor.py
├── scripts/
│   ├── ingest.py
│   ├── clean.py
│   ├── load_database.py
│   ├── create_analytics.py
│   └── pipeline.py
├── tests/
├── api.py
├── dashboard.py
├── Dockerfile
├── requirements.txt
├── .env.example
├── data_dictionary.txt
├── dataset_source.txt
└── README.md
```

## Dataset

- **Source:** UCI Machine Learning Repository — Student Performance dataset.
- **File used:** `student-mat.csv` (Mathematics subject).
- **Original dataset size:** 395 records and 33 attributes.
- **Source format:** semicolon-separated CSV.
- **Expected local path:** `data/student-mat.csv`.

The source dataset is not bundled as a normal CSV in this repository snapshot; it is represented by a DVC pointer. Obtain it through the configured DVC remote if you have access, or download the UCI dataset and place `student-mat.csv` in the `data/` directory.

## Data processing

The ETL runner performs these operations in order:

1. **Ingestion:** reads `data/student-mat.csv` and writes `data/raw/student_raw.csv`.
2. **Staging:** copies the raw CSV to `data/staging/student_staging.csv`.
3. **Cleaning:** removes duplicate rows, validates numeric grade/absence fields, and writes invalid rows to `data/errors/rejected_records.csv`.
4. **Feature creation:** calculates `average_marks = (G1 + G2 + G3) / 3`.
5. **Risk assignment:** assigns High, Medium or Low using the thresholds below.
6. **Database load:** replaces the SQLite `students` table with the cleaned records.
7. **Analytics:** creates/replaces the `student_performance_summary` table.

### Academic-risk rules

| Category | Rule |
|---|---|
| High | `G3 < 10` **OR** `absences > 15` |
| Medium | If not High: `G3 < 14` **OR** `absences > 10` |
| Low | All remaining records |

High is evaluated first, then Medium. These are project-defined thresholds, not labels supplied by UCI or validated dropout outcomes.

## Machine-learning workflow

The model comparison uses these input features:

`age`, `studytime`, `failures`, `absences`, `G1`, `G2`

Target: `risk_level`.

The data is split using an 80/20 train-test split with `random_state=42` and stratification. The compared classifiers are:

- Logistic Regression (with StandardScaler).
- Random Forest (100 trees).
- XGBoost (100 estimators, max depth 4, learning rate 0.1).

Metrics logged to MLflow include accuracy, weighted precision, weighted recall and weighted F1-score.

The README in the original repository reported the following historical comparison results:

| Model | Previously reported accuracy |
|---|---:|
| Logistic Regression | 78.48% |
| Random Forest | 86.08% |
| XGBoost | 87.34% |

These values are historical repository-reported results, not guaranteed results for every run. Re-run the comparison to produce current metrics. Since the target is rule-derived, these scores measure agreement with the project's risk rules, not real-world dropout prediction accuracy.

The selected XGBoost artifact is saved as a bundle containing the model, fitted label encoder and feature names. This keeps the API's class decoding aligned with the trained model.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/adiH2209/Student-Performance-MLOps.git
cd Student-Performance-MLOps
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux / WSL / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Add the dataset

Place `student-mat.csv` at:

```text
data/student-mat.csv
```

The CSV must be the UCI Mathematics dataset and use semicolon separators. If you use DVC instead, configure the remote and retrieve the tracked data with `dvc pull`.

## Run the project

Run all ETL steps from the repository root:

```bash
python scripts/pipeline.py
```

This creates the raw, staging, cleaned and error CSV files, loads `database/students.db`, and creates the analytical summary table.

### Start the dashboard

```bash
streamlit run dashboard.py
```

Streamlit prints a local URL, normally `http://localhost:8501`.

### Compare models and track experiments

Start the MLflow tracking server in Terminal 1:

```bash
mlflow server --host 127.0.0.1 --port 5000
```

Run model comparison in Terminal 2:

```bash
python ml/compare_models.py
```

Open `http://localhost:5000` to view the experiment. The comparison script saves the XGBoost model bundle to `ml/model/student_risk_model.pkl`.

### Start the prediction API

After training a model:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

- API root: `http://localhost:8000/`
- Health check: `http://localhost:8000/health`
- Interactive API docs: `http://localhost:8000/docs`

Example request body for `POST /predict`:

```json
{
  "age": 18,
  "studytime": 2,
  "failures": 0,
  "absences": 4,
  "G1": 12,
  "G2": 13
}
```

Example response:

```json
{
  "predicted_risk": "Low",
  "latency_ms": 2.5,
  "status": "success"
}
```

The predicted category and latency will depend on the trained model and the machine running the API.

### Run monitoring

Make a few API predictions first, then run:

```bash
python monitoring/monitor.py
```

The script summarizes reference-data quality, prediction categories, mean logged latency and a two-sample Kolmogorov–Smirnov feature-distribution check. The drift check is a basic statistical signal; it is not a direct measure of model accuracy. Real performance monitoring requires ground-truth outcomes for logged predictions.

## Docker: API service

The Dockerfile packages the FastAPI service and its trained model. Train the model before building the image, because the model artifact is generated locally and is not committed as a normal binary file.

```bash
python ml/compare_models.py
docker build -t student-academic-risk-api .
docker run --rm -p 8000:8000 student-academic-risk-api
```

Then visit `http://localhost:8000/docs`.

The container currently runs the API only. The database, dashboard and MLflow tracking server are not included in this single-container image.

## Configuration and secrets

- Do not commit real passwords, tokens or API keys.
- Copy `.env.example` to `.env` only if you add environment-based settings.
- Keep `.env` out of Git.
- Rotate any credential that was previously committed or shared. Removing it from the latest file does not erase it from Git history.

## Known limitations

1. The risk target is derived from final grade and absences; it is not a verified dropout outcome.
2. The dataset is small (395 records), so results should be interpreted cautiously.
3. The included pipeline is a Python script, not an Airflow DAG.
4. SQLite is used consistently by the ETL scripts and dashboard in this version.
5. The monitoring script checks feature distributions and prediction logs. It cannot calculate real production accuracy without later ground-truth labels.
6. The DVC pointer files require access to the corresponding DVC remote to retrieve the exact tracked artifacts.
7. The model artifact is generated by running the training/comparison script and is not expected to exist in a fresh clone until that step is completed.

## Suggested next steps

- Obtain genuine dropout/retention outcome labels if the goal is actual dropout prediction.
- Use time-aware validation so model inputs are collected before the outcome.
- Add automated tests and continuous integration.
- Configure a shared DVC remote for reproducible data/model retrieval.
- Add authentication and access controls before using real student records.

## Author

**Aditya Harikumar**

Student project — Data Engineering and MLOps
