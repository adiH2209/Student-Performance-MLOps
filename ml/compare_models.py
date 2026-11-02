from pathlib import Path
import sys
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ml.model_utils import load_data, FEATURES, RANDOM_STATE, build_model, save_bundle

def main():
    df = load_data()
    X = df[FEATURES]
    encoder = LabelEncoder()
    y = encoder.fit_transform(df["risk_level"].astype(str))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    models = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))
        ]),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
        "XGBoost": build_model()
    }
    tracking_uri = __import__("os").environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("Student Academic Risk Classification")
    results = []
    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            model.fit(X_train, y_train)
            pred = model.predict(X_test)
            metrics = {
                "accuracy": accuracy_score(y_test, pred),
                "precision_weighted": precision_score(y_test, pred, average="weighted", zero_division=0),
                "recall_weighted": recall_score(y_test, pred, average="weighted", zero_division=0),
                "f1_weighted": f1_score(y_test, pred, average="weighted", zero_division=0)
            }
            mlflow.log_param("model", name)
            mlflow.log_param("test_size", 0.2)
            mlflow.log_param("random_state", RANDOM_STATE)
            for key, value in metrics.items():
                mlflow.log_metric(key, float(value))
            if name == "XGBoost":
                mlflow.log_params({"n_estimators": 100, "max_depth": 4, "learning_rate": 0.1})
                mlflow.xgboost.log_model(model, name="model")
                bundle = {"model": model, "label_encoder": encoder, "features": FEATURES, "model_name": "XGBoost"}
                save_bundle(bundle)
                print("Saved XGBoost model bundle with its label encoder.")
            else:
                mlflow.sklearn.log_model(
    model,
    name="model",
    skops_trusted_types=["sklearn.tree._tree.Tree"]
)
            results.append((name, metrics))
    print("\nMODEL COMPARISON")
    for name, metrics in results:
        print(f"\n{name}")
        for key, value in metrics.items():
            print(f"{key}: {value:.4f}")
    print("\nComparison completed. XGBoost bundle saved for API use.")

if __name__ == "__main__":
    main()
