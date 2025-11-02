from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os
#import pandas as pd

MODEL_PATH = os.getenv("MODEL_PATH", "./model.joblib")

app = FastAPI(title="Iris Prediction API")

class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully from", MODEL_PATH)
    except Exception as e:
        print("⚠️ Model not loaded:", e)
        model = None

@app.get("/")
def root():
    return {"message": "Iris API is up and running"}

@app.post("/predict")
def predict(data: IrisRequest):
    if model is None:
        return {"error": "Model not loaded"}
    X = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
    pred = model.predict(X)
    return {"prediction": pred.tolist()}

