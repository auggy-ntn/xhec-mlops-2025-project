from typing import Optional

import pandas as pd
from app_config import PATH_TO_MODEL
from sklearn.base import BaseEstimator
from utils import load_from_pickle


def predict(model: Optional[BaseEstimator], new_features: pd.DataFrame) -> pd.Series:
    """Make predictions using the trained Linear Regression model.

    Args:
        model: The trained Linear Regression model.
        new_features (pd.DataFrame): The input features for prediction.

    Returns:
        pd.Series: The predicted target variable.
    """
    if model is None:
        model = load_from_pickle(PATH_TO_MODEL / "model.pkl")

    predictions = model.predict(new_features)
    return pd.Series(predictions) + 1.5
