FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi \
    "uvicorn[standard]" \
    pandas \
    pydantic \
    joblib \
    scikit-learn \
    xgboost \
    scipy

COPY api.py .
COPY monitoring/ monitoring/
COPY ml/model/student_risk_model.pkl ml/model/student_risk_model.pkl

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
