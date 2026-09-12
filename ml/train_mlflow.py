import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load cleaned data
data = pd.read_csv(
    "data/cleaned/student_cleaned.csv"
)


# Features
X = data[
    [
        "age",
        "studytime",
        "failures",
        "absences",
        "G1",
        "G2"
    ]
]


# Target
y = data["risk_level"]


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# MLflow experiment
mlflow.set_tracking_uri("http://localhost:5000")

mlflow.set_experiment(
    "Student Risk Prediction"
)


with mlflow.start_run():

    # Create model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    # Train
    model.fit(
        X_train,
        y_train
    )

    # Predict
    y_pred = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    # Log parameters
    mlflow.log_param(
        "model",
        "RandomForest"
    )

    mlflow.log_param(
        "n_estimators",
        100
    )

    mlflow.log_param(
        "test_size",
        0.2
    )

    # Log metric
    mlflow.log_metric(
        "accuracy",
        accuracy
    )

    # Log model
    mlflow.sklearn.log_model(
        model,
        "student_risk_model"
    )

    print("================================")
    print("MLflow Training Completed")
    print("================================")

    print(
        "Accuracy:",
        round(accuracy, 4)
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            y_pred
        )
    )

    print("\nMLflow experiment logged successfully!")
