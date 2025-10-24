# Use this module to code a `pickle_object` function. This will be useful to pickle the model (and encoder if need be).

import pickle as pkl
from pathlib import Path
from typing import Any

import pandas as pd
from prefect import task

from .config import DATA_DIR


def get_kaggle_data() -> None:
    """Download dataset from Kaggle and save it locally."""
    pass


@task(name="load-data", retries=2)
def load_data(file_path: str = DATA_DIR / "abalone.csv") -> pd.DataFrame:
    """Load the dataset from a local CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The loaded dataset.
    """
    return pd.read_csv(file_path)


@task(name="save-to-pickle")
def save_to_pickle(obj: Any, file_path: str) -> None:
    """Save an object to a specified file path in pickle format.

    Args:
        obj (object): The object to pickle.
        file_path (str): The file path where the object will be saved.

    Returns:
        None
    """
    file_path = Path(file_path)
    # Create parent directories if they don't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("wb") as f:
        pkl.dump(obj, f)


@task(name="load-from-pickle", retries=2)
def load_from_pickle(file_path: str) -> Any:
    """Load an object from a specified pickle file.

    Args:
        file_path (str): The file path from which the object will be loaded.

    Returns:
        Any: The unpickled object.
    """
    with Path.open(file_path, "rb") as f:
        obj = pkl.load(f)
    return obj
