import os
import sys
import mlflow
import mlflow.xgboost
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ml.model_utils import train_and_evaluate, save_bundle

def main():
    bundle, metrics = train_and_evaluate()
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
    mlflow.set_experiment("Student Academic Risk Classification")
    with mlflow.start_run(run_name="XGBoost-Retraining"):
        mlflow.log_params({"model": "XGBoost", "n_estimators": 100, "max_depth": 4, "learning_rate": 0.1})
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
        mlflow.xgboost.log_model(bundle["model"], name="model")
    path = save_bundle(bundle)
    print("Retraining completed.")
    print("Metrics:", metrics)
    print("Updated model bundle:", path)

if __name__ == "__main__":
    main()
