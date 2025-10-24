#!/bin/bash

# Start the Prefect server in the background
uv run prefect server start --host 0.0.0.0 &

# Wait for Prefect server to be ready (check if API is available)
echo "Waiting for Prefect server to start..."
sleep 10
echo "Prefect server is ready!"

# Now start the deployment
uv run python -m src.modelling.deploy &

# Start the MLflow UI
uv run mlflow ui --host 0.0.0.0 --port 5000 &
echo "Backend services (Prefect and MLflow) are up and running."

# URLs:
echo "Prefect UI: http://localhost:4200"
echo "MLflow UI: http://localhost:5000"

# Keep the container running by waiting for all background processes
wait
