import os
import time
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from monitoring.monitor import log_prediction

ROOT = Path(__file__).resolve().parent
MODEL_PATH = Path(os.environ.get("MODEL_PATH", ROOT / "ml" / "model" / "student_risk_model.pkl"))
app = FastAPI(
    title="Student Academic Risk API",
    description="Classifies project-defined academic-risk categories (not verified dropout outcomes).",
    version="1.0.0"
)
model_bundle = None

class StudentData(BaseModel):
    age: int = Field(ge=15, le=25)
    studytime: int = Field(ge=1, le=4)
    failures: int = Field(ge=0, le=4)
    absences: int = Field(ge=0)
    G1: int = Field(ge=0, le=20)
    G2: int = Field(ge=0, le=20)

@app.on_event("startup")
def load_model():
    global model_bundle
    if not MODEL_PATH.exists():
        raise RuntimeError(
            f"Model file not found: {MODEL_PATH}. Run `python ml/compare_models.py` or `python ml/train_model.py` first."
        )
    loaded = joblib.load(MODEL_PATH)
    # Backward compatibility for the older bare-model artifact.
    if isinstance(loaded, dict) and "model" in loaded:
        model_bundle = loaded
    else:
        model_bundle = {"model": loaded, "label_encoder": None, "features": ["age", "studytime", "failures", "absences", "G1", "G2"]}

@app.get("/")
def home():
    return {"message": "Student Academic Risk API is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model_bundle is not None}

@app.post("/predict")
def predict(data: StudentData):
    if model_bundle is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    started = time.perf_counter()
    payload = data.model_dump()
    features = model_bundle.get("features")
    frame = pd.DataFrame([{key: payload[key] for key in features}], columns=features)
    raw_prediction = model_bundle["model"].predict(frame)[0]
    encoder = model_bundle.get("label_encoder")
    if encoder is not None:
        predicted_risk = str(encoder.inverse_transform([int(raw_prediction)])[0])
    else:
        # Legacy model compatibility only; new model bundles store the encoder.
        legacy_mapping = {0: "High", 1: "Low", 2: "Medium"}
        predicted_risk = legacy_mapping.get(int(raw_prediction), str(raw_prediction))
    latency = round((time.perf_counter() - started) * 1000, 2)
    try:
        log_prediction(payload, predicted_risk, latency)
    except Exception:
        # Prediction remains available even if optional local logging fails.
        pass
    return {"predicted_risk": predicted_risk, "latency_ms": latency, "status": "success"}
