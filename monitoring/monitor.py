from pathlib import Path
import pandas as pd
from scipy.stats import ks_2samp

ROOT = Path(__file__).resolve().parents[1]
LOG_FILE = ROOT / "monitoring" / "predictions.csv"
DATA_FILE = ROOT / "data" / "cleaned" / "student_cleaned.csv"
FEATURES = ["age", "studytime", "failures", "absences", "G1", "G2"]

def log_prediction(data, prediction, latency_ms=None):
    row = dict(data)
    row["predicted_risk"] = prediction
    row["latency_ms"] = latency_ms
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(
        LOG_FILE, mode="a", header=not LOG_FILE.exists(), index=False
    )

def monitor_predictions():
    print("=" * 48)
    print("STUDENT ACADEMIC RISK MONITORING")
    print("=" * 48)
    if not DATA_FILE.exists():
        raise FileNotFoundError("Cleaned data missing. Run scripts/pipeline.py first.")
    reference = pd.read_csv(DATA_FILE)
    print("\n1. REFERENCE DATA QUALITY")
    print("Records:", len(reference))
    print("Missing feature values:", int(reference[FEATURES].isna().sum().sum()))
    print("Duplicate records:", int(reference.duplicated().sum()))
    invalid = sum(int(((reference[c] < 0) | (reference[c] > 20)).sum()) for c in ["G1", "G2"])
    print("Invalid G1/G2 values:", invalid)

    if not LOG_FILE.exists():
        print("\nNo prediction log found. Make API predictions to create one.")
        return
    predictions = pd.read_csv(LOG_FILE)
    print("\n2. PREDICTION SUMMARY")
    print("Logged predictions:", len(predictions))
    if "predicted_risk" in predictions:
        print(predictions["predicted_risk"].value_counts(dropna=False).to_string())
    if "latency_ms" in predictions and predictions["latency_ms"].notna().any():
        print("Mean API latency (ms):", round(predictions["latency_ms"].mean(), 2))

    print("\n3. FEATURE DISTRIBUTION CHECK (two-sample KS test)")
    if len(predictions) < 2:
        print("At least two logged predictions are required.")
        return
    for feature in FEATURES:
        if feature not in predictions:
            continue
        ref = pd.to_numeric(reference[feature], errors="coerce").dropna()
        current = pd.to_numeric(predictions[feature], errors="coerce").dropna()
        if len(current) < 2 or ref.empty:
            print(f"{feature}: insufficient numeric values")
            continue
        _, p_value = ks_2samp(ref, current)
        status = "POTENTIAL DISTRIBUTION SHIFT" if p_value < 0.05 else "No significant shift detected"
        print(f"{feature}: {status} (p={p_value:.4f})")
    print("\nNote: a feature-distribution test is not a measure of model accuracy.")
    print("True production performance requires ground-truth outcomes for predictions.")

if __name__ == "__main__":
    monitor_predictions()
