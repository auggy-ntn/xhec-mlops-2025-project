#!/bin/bash

# Start the FastAPI app
uv run uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 &
echo "All services are up and running."

# URLs:
echo "FastAPI App: http://localhost:8001/docs"

# Keep the container running by waiting for all background processes
wait
