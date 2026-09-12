import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
import mlflow.xgboost

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier

DATA_PATH = "data/cleaned/student_cleaned.csv"

df = pd.read_csv(DATA_PATH)

features = [
    "age",
    "studytime",
    "failures",
    "absences",
    "G1",
    "G2"
]
X = df[features]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["risk_level"])

print("Class mapping:", dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_))))
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),

    "XGBoost": XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        objective="multi:softmax",
        num_class=3,
        eval_metric="mlogloss",
        random_state=42
    )
}

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Student Risk Prediction")

for name, model in models.items():

    with mlflow.start_run(run_name=name):

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        mlflow.log_param("model", name)
        mlflow.log_param("test_size", 0.2)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1_score", f1)

        if name == "Random Forest":
            mlflow.log_param("n_estimators", 100)

        if name == "XGBoost":
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 4)
            mlflow.log_param("learning_rate", 0.1)

        if name == "XGBoost":
            mlflow.xgboost.log_model(model, name="student_risk_model")
        else:
            mlflow.sklearn.log_model(model, name="student_risk_model")
        if name == "XGBoost":
            joblib.dump(model, "ml/model/student_risk_model.pkl")
            print("XGBoost saved as final deployed model.")

        print("\n" + name)
        print("----------------------")
        print("Accuracy :", round(accuracy, 4))
        print("Precision:", round(precision, 4))
        print("Recall   :", round(recall, 4))
        print("F1 Score :", round(f1, 4))

print("\nModel comparison completed successfully.")
