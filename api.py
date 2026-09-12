from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from monitoring.monitor import log_prediction
app = FastAPI(title="Student Risk Prediction API")

model = joblib.load("ml/model/student_risk_model.pkl")


class StudentData(BaseModel):
    age: int
    studytime: int
    failures: int
    absences: int
    G1: int
    G2: int


@app.get("/")
def home():
    return {"message": "Student Risk Prediction API is running"}


@app.post("/predict")
def predict(data: StudentData):
    input_data = pd.DataFrame([{
        "age": data.age,
        "studytime": data.studytime,
        "failures": data.failures,
        "absences": data.absences,
        "G1": data.G1,
        "G2": data.G2
    }])

    prediction = model.predict(input_data)[0]

    log_prediction(data.model_dump(), str(prediction))
    return {
        "predicted_risk": str(prediction)
    }
