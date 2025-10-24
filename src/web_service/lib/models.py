from enum import Enum

from pydantic import BaseModel, NonNegativeFloat


class SexOptions(str, Enum):
    MALE = "M"
    FEMALE = "F"
    INFANT = "I"


class InputData(BaseModel):
    Sex: SexOptions
    Length: NonNegativeFloat
    Diameter: NonNegativeFloat
    Height: NonNegativeFloat
    Whole_weight: NonNegativeFloat
    Shucked_weight: NonNegativeFloat
    Viscera_weight: NonNegativeFloat
    Shell_weight: NonNegativeFloat


class PredictionOut(BaseModel):
    age: NonNegativeFloat
