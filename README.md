# Student Performance & Academic-Risk Classification

A Python project that processes the UCI Student Performance Mathematics dataset, derives project-defined academic-risk categories, compares classification models, tracks experiments with MLflow, stores processed data in PostgreSQL, and provides a Streamlit dashboard and FastAPI prediction service. Apache Airflow can orchestrate the ETL workflow, Docker Compose runs the services, and DVC manages dataset/model artifacts.

> **Target definition:** `risk_level` is derived from final grade (`G3`) and absences using the thresholds below. The UCI dataset does not provide a verified future dropout outcome. This is academic-risk classification, not a validated student-dropout prediction system.

## Technology stack

| Layer | Tools |
|---|---|
| Language | Python 3.11 |
| Data processing | Pandas, NumPy |
| Machine learning | Scikit-learn, XGBoost |
| Algorithms | Logistic Regression, Random Forest, XGBoost |
| Experiment tracking | MLflow |
| Database | PostgreSQL |
| Dashboard | Streamlit, Plotly |
| API | FastAPI, Uvicorn, Pydantic |
| Monitoring | Pandas, SciPy |
| Workflow orchestration | Apache Airflow |
| Data/model versioning | DVC |
| Containerization | Docker, Docker Compose |
| Version control | Git, GitHub |

## Architecture

```text
UCI student-mat.csv --DVC--> scripts/ingest.py -> stage.py -> clean.py
                                                    |
                                                    v
                                           cleaned CSV dataset
                                                    |
                                  +-----------------+----------------+
                                  |                                  |
                                  v                                  v
                         PostgreSQL database                ML comparison
                                  |                      Logistic Regression
                                  |                      Random Forest
                                  |                      XGBoost
                                  |                                  |
                                  v                                  v
                         Streamlit dashboard                  MLflow tracking
                                                                     |
                                                                     v
                                                         model artifact (DVC)
                                                                     |
                                                                     v
                                                               FastAPI

Airflow DAG orchestrates ingest -> stage -> clean -> PostgreSQL load -> analytics.
Docker Compose runs PostgreSQL, Airflow, API and dashboard services.
```

## Repository layout

```text
├── dags/student_performance_pipeline.py  # Airflow ETL DAG
├── data/                                  # Dataset and generated ETL files
├── dvc-storage/                           # Local DVC remote (ignored; populate with dvc push)
├── ml/                                    # Training, comparison and model utilities
├── monitoring/                            # Prediction and feature monitoring
├── scripts/                               # Ingest, stage, clean, PostgreSQL load, analytics
├── tests/                                 # Unit tests
├── api.py                                 # FastAPI prediction API
├── dashboard.py                           # Streamlit dashboard
├── Dockerfile                             # API/dashboard image
├── Dockerfile.airflow                     # Airflow image with ETL dependencies
├── docker-compose.yml                     # PostgreSQL + Airflow + optional app services
├── requirements.txt
└── README.md
```

## Dataset and DVC

The project uses the UCI Student Performance Mathematics file `student-mat.csv` (395 records, 33 attributes). Place the file at `data/student-mat.csv`.

DVC is configured with a **local remote** at `dvc-storage/` so the workflow can be demonstrated without inventing cloud credentials. The `.dvc` pointer file alone does not contain the dataset. After placing the dataset locally, track and upload it to the local DVC remote:

```bash
dvc add data/student-mat.csv
dvc push
```

For another machine, share/copy the `dvc-storage/` directory or configure a shared remote (S3, Azure, SSH, etc.) and commit the updated `.dvc/config` appropriately. Do not commit credentials.

After training creates `ml/model/student_risk_model.pkl`, track it similarly:

```bash
dvc add ml/model/student_risk_model.pkl
dvc push
```

## Academic-risk rules

| Category | Rule |
|---|---|
| High | `G3 < 10` OR `absences > 15` |
| Medium | If not High: `G3 < 14` OR `absences > 10` |
| Low | All remaining records |

These are project-defined labels, not labels supplied by UCI or independently validated dropout outcomes.

## ML workflow

Input features: `age`, `studytime`, `failures`, `absences`, `G1`, `G2`. Target: `risk_level`.

The comparison script trains Logistic Regression (with scaling), Random Forest and XGBoost using an 80/20 stratified split (`random_state=42`). MLflow records model parameters and evaluation metrics. Re-run training to obtain current scores; previously reported README accuracies are historical results and are not guaranteed to reproduce exactly.

## Local setup

1. Install Python 3.11 and PostgreSQL.
2. Create a database and user, or use the Compose setup below.
3. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

4. Set `DATABASE_URL` (PowerShell example):

```powershell
$env:DATABASE_URL="postgresql+psycopg2://student:studentpass@localhost:5432/student_performance"
```

5. Put `student-mat.csv` in `data/` and run:

```bash
python scripts/pipeline.py
python ml/compare_models.py
```


## Model Performance

The following models were trained and evaluated using an 80:20 train-test split.

| Model | Accuracy | Weighted Precision | Weighted Recall | Weighted F1-Score |
|---|---:|---:|---:|---:|
| Logistic Regression | 78.48% | 78.96% | 78.48% | 78.64% |
| Random Forest | 86.08% | 86.56% | 86.08% | 86.16% |
| XGBoost | **87.34%** | **87.43%** | **87.34%** | **87.36%** |

### Best Performing Model

XGBoost achieved the highest accuracy of **87.34%**, outperforming Logistic Regression and Random Forest. Therefore, XGBoost is selected as the final model for student academic risk prediction.

6. Start the dashboard:

```bash
streamlit run dashboard.py
```

7. Start the API after the model has been trained:

```bash
uvicorn api:app --reload
```

## Airflow with Docker Compose

The Compose stack starts a PostgreSQL application database, a separate PostgreSQL Airflow metadata database, and Airflow webserver/scheduler. It does not automatically download the dataset or train the model.

```bash
docker compose up airflow-init
docker compose up -d postgres airflow-db airflow-webserver airflow-scheduler
```

Open `http://localhost:8080`. Airflow's default standalone image credentials are not assumed here; create an admin user explicitly if needed:

```bash
docker compose run --rm airflow-webserver airflow users create --username admin --password admin --firstname Project --lastname Admin --role Admin --email admin@example.com
```

Enable and trigger `student_performance_etl`. The dataset must already exist at `data/student-mat.csv` in the project directory. The DAG runs ingest, staging, cleaning, PostgreSQL load and analytics in order.

## Docker services

After the dataset is loaded and model artifact is trained, start the optional API and dashboard services:

```bash
docker compose --profile app up --build -d
```

- Dashboard: `http://localhost:8501`
- API docs: `http://localhost:8000/docs`
- Airflow: `http://localhost:8080`

The API requires `ml/model/student_risk_model.pkl`. Train it before starting the API container. Change the example passwords and Airflow secret key before using this beyond a local demonstration. Never commit real credentials or `.env` files.

## Notes

- Airflow orchestration is implemented in `dags/student_performance_pipeline.py`; `scripts/pipeline.py` remains a local sequential runner.
- PostgreSQL is the only application database in this version; SQLite has been removed.
- DVC uses a local remote by default. It is not a hosted remote until configured by the project owner.
- Docker Compose is provided for local demonstration; production deployment requires secrets management, persistent backups, and security hardening.



