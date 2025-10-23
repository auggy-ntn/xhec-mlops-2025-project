from pydantic import BaseModel


class InputData(BaseModel):
    Feature1: int
    Feature2: int
    Feature3: int


class PredictionOut(BaseModel):
    age: float
