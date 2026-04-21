from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

from app.services.model_service import run_prediction

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/predict")
def predict():
    return run_prediction()