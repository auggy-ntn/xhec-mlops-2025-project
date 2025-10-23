# Configuration settings for the project

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
print(f"Project root set to: {PROJECT_ROOT}")
print(f"Data directory set to: {DATA_DIR}")
print(f"Model directory set to: {MODEL_DIR}")

NUMERICAL_COLS = [
    "Length",
    "Diameter",
    "Height",
    "Whole weight",
    "Shucked weight",
    "Viscera weight",
    "Shell weight",
]
