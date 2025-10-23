# Code with FastAPI (app = FastAPI(...))


from fastapi import FastAPI

from web_service.lib.models import InputData, PredictionOut

app = FastAPI(title="...", description="...")


@app.get("/")
def home() -> dict:
    return {"health_check": "App up and running!"}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(input: InputData) -> dict:
    ##
    ##
    ##
    return {"Predicted age of the abalone"}
