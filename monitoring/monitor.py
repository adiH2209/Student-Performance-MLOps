import pandas as pd
from pathlib import Path

LOG_FILE = Path("monitoring/predictions.csv")


def log_prediction(data, prediction):
    row = data.copy()
    row["predicted_risk"] = prediction

    df = pd.DataFrame([row])

    if LOG_FILE.exists():
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)


def monitor_predictions():
    if not LOG_FILE.exists():
        print("No prediction data available.")
        return

    df = pd.read_csv(LOG_FILE)

    print("\nPrediction Monitoring")
    print("---------------------")
    print("Total predictions:", len(df))

    print("\nRisk distribution:")
    print(df["predicted_risk"].value_counts())

    print("\nMonitoring completed.")


if __name__ == "__main__":
    monitor_predictions()
