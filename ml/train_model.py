import pandas as pd
import joblib

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


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# Train model
model.fit(
    X_train,
    y_train
)


# Predict test data
y_pred = model.predict(X_test)


# Accuracy
accuracy = accuracy_score(
    y_test,
    y_pred
)


print("================================")
print("Student Risk Prediction Model")
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


# Save model
joblib.dump(
    model,
    "ml/model/student_risk_model.pkl"
)


print("\nModel saved successfully!")
print(
    "Location: ml/model/student_risk_model.pkl"
)
