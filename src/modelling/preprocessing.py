# Preprocessing functions for the abalone dataset.

from typing import Optional, Tuple

import pandas as pd
from prefect import task
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .config import NUMERICAL_COLS


def create_preprocessor() -> ColumnTransformer:
    """Create a preprocessor that handles both one-hot encoding and scaling.

    Returns:
        ColumnTransformer: A preprocessor that one-hot encodes 'Sex' and scales numerical features.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("onehot", OneHotEncoder(drop="first", sparse_output=False), ["Sex"]),
            ("scaler", StandardScaler(), NUMERICAL_COLS),
        ],
        remainder="passthrough",
    )
    return preprocessor


@task(name="preprocess-data")
def preprocess_data(
    df: pd.DataFrame,
    preprocessor: Optional[ColumnTransformer] = None,
    with_target: bool = True,
) -> Tuple[pd.DataFrame, Optional[pd.Series], ColumnTransformer]:
    """Preprocess the abalone dataset using a unified preprocessor.

    Args:
        df (pd.DataFrame): The input dataframe with all columns.
        preprocessor (Optional[ColumnTransformer], optional): An existing preprocessor to use.
            If None, a new preprocessor will be created and fitted. Defaults to None.
        with_target (bool, optional): Whether to separate the target variable 'Rings' from the features. Defaults to True.

    Returns:
        Tuple[pd.DataFrame, Optional[pd.Series], ColumnTransformer]: A tuple containing the preprocessed dataframe,
            the target variable (if with_target is True), and the preprocessor used.
    """
    df = df.copy()
    df = df.rename(columns=lambda x: x.replace(" ", "_"))

    if with_target:
        y = df["Rings"]
        X = df.drop("Rings", axis=1)
    else:
        y = None
        X = df

    if preprocessor is None:
        preprocessor = create_preprocessor()
        X_processed = preprocessor.fit_transform(X)
    else:
        X_processed = preprocessor.transform(X)

    # Get feature names after transformation
    feature_names = []
    for name, transformer, columns in preprocessor.transformers_:
        if name == "onehot":
            feature_names.extend(transformer.get_feature_names_out(columns))
        elif name == "scaler":
            feature_names.extend(columns)
        elif name != "remainder":
            feature_names.extend(columns)

    X_processed_df = pd.DataFrame(X_processed, columns=feature_names, index=X.index)

    return X_processed_df, y, preprocessor
