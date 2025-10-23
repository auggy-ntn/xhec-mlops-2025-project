import pickle as pkl
from pathlib import Path
from typing import Any


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
