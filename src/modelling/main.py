# This module is the training flow: it reads the data, preprocesses it, trains a model and saves it.

import argparse
from datetime import datetime
from pathlib import Path

import mlflow
from prefect import flow, get_run_logger
from sklearn.metrics import mean_squared_error, r2_score

from .config import DATA_DIR
from .predicting import predict
from .preprocessing import preprocess_data
from .training import train_model
from .utils import load_data, save_to_pickle


@flow(name="training-pipeline", log_prints=True)
def main(
    trainset_path: Path = DATA_DIR / "abalone.csv",
    stage: str = "Production",
) -> None:
    """Train a model using the data at the given path and save the model (pickle).

    This is the main training flow that orchestrates all the training tasks.

    Args:
        trainset_path: Path to the training dataset
        stage: The stage to register the model under in MLflow Model Registry
    """
    logger = get_run_logger()

    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    # Set MLflow tracking URI to src/mlruns directory
    mlflow.set_tracking_uri("file:./src/mlruns")
    mlflow.set_experiment("Abalone Age Prediction Model Training")

    with mlflow.start_run() as run:
        tags = {
            "Run Name": "Abalone Model Training Flow",
            "Date": date,
            "Time": time,
        }
        mlflow.set_tags(tags)

        # Read data
        logger.info(f"Loading data from {trainset_path}")
        df = load_data(trainset_path)

        # Log dataset info
        mlflow.log_param("dataset_size", len(df))
        mlflow.log_param("num_features", len(df.columns) - 1)

        # Preprocess data
        logger.info("Preprocessing data")
        x, y, preprocessor = preprocess_data(df)

        # Save preprocessor
        logger.info(
            "Saving preprocessor to src/web_service/local_objects/preprocessor.pkl"
        )
        save_to_pickle(preprocessor, "src/web_service/local_objects/preprocessor.pkl")
        mlflow.sklearn.log_model(preprocessor, "preprocessor")
        logger.info("Preprocessor logged to MLflow")

        # Train model
        logger.info("Training model")
        model = train_model(x, y)
        params = model.get_params()
        mlflow.log_params(params)

        # Evaluate model on training set (to log to MLflow)
        y_pred = predict(model, x)
        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)
        mlflow.log_metric("train_mse", mse)
        mlflow.log_metric("train_r2", r2)
        logger.info(f"Training MSE: {mse:.4f}, R2: {r2:.4f}")

        # Pickle model --> The model should be saved in pkl format the `src/web_service/local_objects` folder
        logger.info("Saving trained model to src/web_service/local_objects/model.pkl")
        save_to_pickle(model, "src/web_service/local_objects/model.pkl")

        # Log model to MLflow
        mlflow.sklearn.log_model(model, "model")
        logger.info("Model logged to MLflow")

        # Register the model
        run_id = run.info.run_id
        model_version = mlflow.register_model(
            f"runs:/{run_id}/model", "abalone_age_prediction_model"
        )
        registered_version = model_version.version
        logger.info(f"Model registered as version {registered_version}")

        client = mlflow.MlflowClient()
        client.transition_model_version_stage(
            name="abalone_age_prediction_model", version=registered_version, stage=stage
        )
        logger.info(f"Model version {registered_version} transitioned to {stage} stage")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train a model using the data at the given path."
    )
    parser.add_argument("trainset_path", type=str, help="Path to the training set")
    args = parser.parse_args()
    main(Path(args.trainset_path))
