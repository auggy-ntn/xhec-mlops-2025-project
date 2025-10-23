from app_config import (
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    PATH_TO_MODEL,
    PATH_TO_SCALER,
)
from fastapi import FastAPI
from lib.modelling import predict
from lib.models import InputData, PredictionOut
from utils import load_from_pickle

app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION, version=APP_VERSION)


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predictions(input: InputData) -> dict:
    scaler = load_from_pickle(PATH_TO_SCALER)
    model = load_from_pickle(PATH_TO_MODEL)
    input_data = scaler.transform([input.values()])
    prediction = predict(model, input_data)
    return {f"Predicted age of the abalone:{prediction[0]}"}
