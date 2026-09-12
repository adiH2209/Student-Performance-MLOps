from fastapi import FastAPI
from pydantic import BaseModel
import time
import joblib
import pandas as pd
from monitoring.monitor import log_prediction

app = FastAPI(title="Student Risk Prediction API")

model = joblib.load("ml/model/student_risk_model.pkl")

risk_mapping = {
    0: "High",
    1: "Low",
    2: "Medium"
}


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

    start_time = time.time()

    try:
        input_data = pd.DataFrame([{
            "age": data.age,
            "studytime": data.studytime,
            "failures": data.failures,
            "absences": data.absences,
            "G1": data.G1,
            "G2": data.G2
        }])

        prediction = model.predict(input_data)[0]

        predicted_risk = risk_mapping[int(prediction)]

        log_prediction(
            data.model_dump(),
            predicted_risk
        )

        latency = round((time.time() - start_time) * 1000, 2)

        return {
            "predicted_risk": predicted_risk,
            "latency_ms": latency,
            "status": "success"
        }

    except Exception as e:

        latency = round((time.time() - start_time) * 1000, 2)

        return {
            "status": "failed",
            "error": str(e),
            "latency_ms": latency
        }
