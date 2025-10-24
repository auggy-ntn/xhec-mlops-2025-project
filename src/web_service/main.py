import pandas as pd
from fastapi import FastAPI
from loguru import logger

from src.modelling.predicting import predict
from src.modelling.utils import load_from_pickle
from src.web_service.app_config import (
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    MODELS_DIR,
)
from src.web_service.lib.models import InputData, PredictionOut

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predictions(input: InputData) -> PredictionOut:
    """Make predictions based on input data

    Args:
        input (InputData): The input data for making predictions.

    Returns:
        dict: The prediction results.
    """
    logger.info(f"Received input for prediction: {input}")

    logger.info(f"Loading preprocessor from {MODELS_DIR / 'preprocessor.pkl'}")
    preprocessor = load_from_pickle.fn(
        MODELS_DIR / "preprocessor.pkl"
    )  # fn to not call the Prefect task, just the function

    logger.info(f"Loading model from {MODELS_DIR / 'model.pkl'}")
    model = load_from_pickle.fn(MODELS_DIR / "model.pkl")

    logger.info("Preprocessing input data")
    # Convert Pydantic model to DataFrame
    input_dict = input.model_dump()
    input_df = pd.DataFrame([input_dict])

    # Apply preprocessing
    input_processed = preprocessor.transform(input_df)

    logger.info("Making prediction")
    prediction = predict.fn(model, input_processed)
    logger.info(f"Prediction made: {prediction[0]}")
    return PredictionOut(age=prediction[0])
