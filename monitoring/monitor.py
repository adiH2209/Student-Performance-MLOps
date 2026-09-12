import pandas as pd
import joblib
from pathlib import Path
from scipy.stats import ks_2samp
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

LOG_FILE = Path("monitoring/predictions.csv")
DATA_FILE = Path("data/cleaned/student_cleaned.csv")
MODEL_FILE = Path("ml/model/student_risk_model.pkl")

FEATURES = [
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2",


]
risk_mapping = {
    0: "High",
    1: "Low",
    2: "Medium"
}
def log_prediction(data, prediction):
    row = data.copy()
    row["predicted_risk"] = prediction

    df = pd.DataFrame([row])

    if LOG_FILE.exists():
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)

def monitor_predictions():

    print("\n==============================")
    print("     MLOps Model Monitoring")
    print("==============================")

    # -----------------------------
    # 1. Input Data Quality
    # -----------------------------
    data = pd.read_csv(DATA_FILE)

    print("\n1. INPUT DATA QUALITY")
    print("------------------------------")
    print("Total records:", len(data))
    print("Missing values:", int(data[FEATURES].isnull().sum().sum()))
    print("Duplicate records:", int(data.duplicated().sum()))

    invalid_values = 0

    for column in ["G1", "G2"]:
        invalid_values += int(((data[column] < 0) | (data[column] > 20)).sum())

    print("Invalid mark values:", invalid_values)

    # -----------------------------
    # 2. Prediction Monitoring
    # -----------------------------
    if not LOG_FILE.exists():
        print("\nNo prediction log available.")
        return

    predictions = pd.read_csv(LOG_FILE)

    print("\n2. PREDICTION MONITORING")
    print("------------------------------")
    print("Total predictions:", len(predictions))

    print("\nPrediction class distribution:")
    print(predictions["predicted_risk"].value_counts())

    # -----------------------------
    # 3. Feature Drift
    # -----------------------------
    print("\n3. FEATURE DRIFT")
    print("------------------------------")

    if len(predictions) >= 2:

        drift_found = False

        for feature in FEATURES:

            if feature not in predictions.columns:
                continue

            statistic, p_value = ks_2samp(
                data[feature].dropna(),
                predictions[feature].dropna()
            )

            if p_value < 0.05:
                print(
                    feature,
                    "-> DRIFT DETECTED",
                    "(p-value:",
                    round(p_value, 4),
                    ")"
                )
                drift_found = True
            else:
                print(
                    feature,
                    "-> No significant drift",
                    "(p-value:",
                    round(p_value, 4),
                    ")"
                )

        if not drift_found:
            print("Overall result: No significant feature drift detected.")

    else:
        print("Need at least 2 predictions to calculate drift.")

    # -----------------------------
    # 4. Model Performance
    # -----------------------------
    print("\n4. MODEL PERFORMANCE")
    print("------------------------------")

    model = joblib.load(MODEL_FILE)

    X = data[FEATURES]
    y = data["risk_level"]

    y_pred = model.predict(X)

    y_pred = [risk_mapping[int(pred)] for pred in y_pred]

    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(
        y, y_pred, average="weighted", zero_division=0
    )
    recall = recall_score(
        y, y_pred, average="weighted", zero_division=0
    )
    f1 = f1_score(
        y, y_pred, average="weighted", zero_division=0
    )

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    # -----------------------------
    # 5. Retraining Recommendation
    # -----------------------------
    print("\n5. RETRAINING CRITERIA")
    print("------------------------------")

    if accuracy < 0.80:
        print("RETRAINING RECOMMENDED: Accuracy below 80%.")
    else:
        print("Model performance is acceptable.")

    print("\n==============================")
    print("Monitoring completed.")
    print("==============================")


if __name__ == "__main__":
    monitor_predictions()
