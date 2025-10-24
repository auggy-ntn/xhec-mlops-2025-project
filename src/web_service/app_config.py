from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# MODELS
MODEL_VERSION = "0.0.1"
MODELS_DIR = PROJECT_ROOT / "src" / "web_service" / "local_objects"


# MISC
APP_TITLE = "AgeAbalonePredictionApp"
APP_DESCRIPTION = (
    "A simple API to predict the age of an abalone in years"
    "given its sex and physical measurements"
)
APP_VERSION = "0.0.1"
