import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


DATA_PATH = "data/cleaned/student_cleaned.csv"
MODEL_PATH = "ml/model/student_risk_model.pkl"


# Load data
df = pd.read_csv(DATA_PATH)

# Features used for prediction
features = [
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2"
]

X = df[features]
y = df["risk_level"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train
model.fit(X_train, y_train)


# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Retraining completed.")
print("Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Student Risk Prediction")

with mlflow.start_run(run_name="Retraining"):
    mlflow.log_param("model", "Random Forest")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("test_size", 0.2)

    mlflow.log_metric("accuracy", accuracy)

    mlflow.sklearn.log_model(
        model,
        name="student_risk_model"
    )


# Save updated model
joblib.dump(model, MODEL_PATH)

print("\nUpdated model saved to:", MODEL_PATH)
print("Retraining and MLflow logging completed successfully.")
