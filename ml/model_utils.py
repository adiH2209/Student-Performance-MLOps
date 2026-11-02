from pathlib import Path
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "cleaned" / "student_cleaned.csv"
MODEL_FILE = ROOT / "ml" / "model" / "student_risk_model.pkl"
FEATURES = ["age", "studytime", "failures", "absences", "G1", "G2"]
RANDOM_STATE = 42

def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError("Cleaned dataset missing. Run: python scripts/pipeline.py")
    df = pd.read_csv(DATA_FILE)
    missing = set(FEATURES + ["risk_level"]).difference(df.columns)
    if missing:
        raise ValueError(f"Cleaned dataset is missing columns: {sorted(missing)}")
    return df

def build_model():
    return XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        objective="multi:softprob",
        eval_metric="mlogloss",
        random_state=RANDOM_STATE,
        n_jobs=1
    )

def train_and_evaluate():
    df = load_data()
    X = df[FEATURES]
    encoder = LabelEncoder()
    y = encoder.fit_transform(df["risk_level"].astype(str))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    model = build_model()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision_weighted": float(precision_score(y_test, pred, average="weighted", zero_division=0)),
        "recall_weighted": float(recall_score(y_test, pred, average="weighted", zero_division=0)),
        "f1_weighted": float(f1_score(y_test, pred, average="weighted", zero_division=0))
    }
    bundle = {"model": model, "label_encoder": encoder, "features": FEATURES, "model_name": "XGBoost"}
    return bundle, metrics

def save_bundle(bundle):
    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, MODEL_FILE)
    return MODEL_FILE
