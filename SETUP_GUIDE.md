<div align="center">

# 🚀 Complete Setup Guide
## Abalone Age Prediction MLOps Project

</div>

This comprehensive guide covers the complete setup, structure, and deployment of the Abalone Age Prediction MLOps project.

---

## 📋 Table of Contents

1. [Project Structure](#-project-structure)
2. [Environment Setup](#-environment-setup)
3. [Local Development](#-local-development)
4. [Docker Compose Deployment](#-docker-compose-deployment)
5. [MLFlow UI](#-mlflow-ui)
6. [Prefect UI](#-prefect-ui)
7. [API Usage](#-api-usage)
8. [Troubleshooting](#-troubleshooting)

---

## 📁 Project Structure

```
xhec-mlops-2025-project/
├── src/
│   ├── modelling/              # ML Pipeline code
│   │   ├── main.py            # Entry point for training pipeline
│   │   ├── deploy.py          # Prefect deployment configuration
│   │   ├── training.py        # Model training logic
│   │   ├── preprocessing.py   # Data preprocessing
│   │   ├── predicting.py      # Prediction logic
│   │   ├── utils.py           # Utility functions
│   │   └── config.py          # Configuration settings
│   ├── web_service/           # FastAPI application
│   │   ├── main.py           # FastAPI endpoints
│   │   ├── app_config.py     # API configuration
│   │   ├── lib/
│   │   │   └── models.py     # Pydantic models for API
│   │   └── local_objects/    # Stored models and preprocessors
│   └── mlruns/               # MLFlow experiment tracking
├── data/
│   └── abalone.csv           # Training dataset
├── notebooks/
│   ├── eda.ipynb            # Exploratory Data Analysis
│   ├── modelling.ipynb      # Model development
│   └── mlruns/              # Notebook experiments tracking
├── bin/
│   ├── run_api_service.sh    # API startup script
│   ├── run_backend_service.sh # Backend services startup
│   └── init_data.sh          # Data initialization script
├── docker-compose.yml         # Multi-service orchestration
├── Dockerfile.api             # API service container
├── Dockerfile.backend         # Backend services container
├── pyproject.toml            # Project dependencies and metadata
└── README.md                 # Project documentation
```

### Key Components

- **`src/modelling/`**: Contains the complete ML pipeline orchestrated by Prefect
- **`src/web_service/`**: FastAPI application for serving predictions
- **`bin/`**: Shell scripts for running services in Docker containers
- **`data/`**: Dataset storage
- **`notebooks/`**: Jupyter notebooks for experimentation
- **Docker files**: Containerization configuration for deployment

---

## 🛠️ Environment Setup (for local development)

### Prerequisites

Before starting, ensure you have:

- **Python 3.11** (strictly required)
- **[uv](https://docs.astral.sh/uv/)** package manager
- **Docker** and **Docker Compose** (for containerized deployment)
- **Git** for version control
- **SQLite** (required for Prefect backend)

### Installing uv

```zsh
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```
For Windows, see the [uv documentation](https://docs.astral.sh/uv/getting-started/installation/).

### Initial Setup

1. **Clone the repository**:
   ```zsh
   git clone git@github.com:auggy-ntn/xhec-mlops-2025-project.git
   ```

2. **Install dependencies and create virtual environment**:
   ```zsh
   # This creates a .venv directory and installs all dependencies (including dev dependencies)
   uv sync --all-groups
   ```

3. **Install pre-commit hooks** (for code quality):
   ```zsh
   uv run pre-commit install
   ```

### Dependencies Overview

The project uses the following key dependencies (defined in `pyproject.toml`):

**Production Dependencies:**
- `mlflow>=3.5.1` - Experiment tracking and model registry
- `prefect>=3.0.0` - Workflow orchestration
- `fastapi` - REST API framework
- `scikit-learn>=1.7.2` - Machine learning library
- `pandas>=2.3.3` - Data manipulation
- `pydantic>=2.12.3` - Data validation
- `loguru>=0.7.3` - Logging

**Development Dependencies:**
- `ruff>=0.14.1` - Fast Python linter and formatter
- `pre-commit>=4.3.0` - Git hook management
- `nbstripout>=0.8.1` - Strip Jupyter notebook outputs
- `ipykernel>=7.0.1` - Jupyter kernel

---

## 💻 Local Development

### Running the Complete Pipeline Locally

To run the project locally without Docker, you need to start multiple services.

#### Step 0: Download the data
From [the Kaggle challenge](https://www.kaggle.com/datasets/rodolfomendes/abalone-dataset), download the dataset and place it in the ```data/``` directory located at the project's root. Name it ```abalone.csv```.

#### Step 1: Start Prefect Server

In **Terminal 1**, start the Prefect server:

```zsh
# Configure Prefect API URL (first time only)
uv run prefect config set PREFECT_API_URL=http://0.0.0.0:4200/api

# Start Prefect server
uv run prefect server start --host 0.0.0.0
```

**Access Prefect UI**: http://0.0.0.0:4200

Keep this terminal running!

#### Step 2: Start MLFlow UI

In **Terminal 2**, start the MLFlow tracking UI:

```zsh
# Start MLFlow UI pointing to the src/mlruns directory
uv run mlflow ui --backend-store-uri ./src/mlruns --host 0.0.0.0 --port 5000
```

**Access MLFlow UI**: http://localhost:5000

Keep this terminal running!

#### Step 3: Run Training Pipeline

In **Terminal 3**, run the training workflow:

```zsh
# Run training pipeline with Production stage
uv run python -m src.modelling.main data/abalone.csv Production
```

This will:
- Load and preprocess the `abalone.csv` dataset
- Train a machine learning model
- Log metrics and parameters to MLFlow
- Save the model and preprocessor to `src/web_service/local_objects/`
- Register the model in MLFlow with "Production" stage

#### Step 4: Create Automated Deployment

In **Terminal 4** (optional), set up scheduled retraining:

```zsh
# Run deployment script
uv run python -m src.modelling.deploy
```

This creates a Prefect deployment that:
- Runs daily at 1 AM UTC
- Can be manually triggered from Prefect UI
- Automatically retrains the model

#### Step 5: Start the API

In **Terminal 5**, run the FastAPI application:

```zsh
# Start FastAPI server
uv run uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 --reload
```

**Access API Documentation**: http://localhost:8001/docs

### Local Development URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Prefect UI | http://0.0.0.0:4200 | Workflow orchestration, monitoring, scheduling |
| MLFlow UI | http://localhost:5000 | Experiment tracking, model registry |
| FastAPI Docs | http://localhost:8001/docs | Interactive API documentation |
| API Root | http://localhost:8001 | Health check endpoint |

---

## 🐳 Docker Compose Deployment

The easiest way to run the entire application is using Docker Compose, which orchestrates all services automatically.

### Architecture Overview

The `docker-compose.yml` defines three services:

1. **init-data**: Initializes shared volumes with data, models, and MLFlow runs
2. **ml-backend**: Runs Prefect + MLFlow servers
3. **api**: Serves the FastAPI prediction endpoint

### Prerequisites for Docker Deployment

1. **Docker and Docker Compose installed**:
   ```zsh
   docker --version
   ```

### Deploying with Docker Compose

The simplest approach uses images already pushed to DockerHub:

```zsh
# From project root
docker compose up -d    # (remove the -d flag if you want to see terminal outputs)
```

This will:
- Pull `augustinnaton/abalone-backend:latest`
- Pull `augustinnaton/abalone-api:latest`
- Start all services in detached mode

The images were built locally and pushed to DockerHub, you do not need to build them yourself.

### Accessing Services

Once Docker Compose is running, access:

| Service | URL | Description |
|---------|-----|-------------|
| Prefect UI | http://0.0.0.0:4200 | Monitor training workflows and deployments |
| MLFlow UI | http://localhost:5000 | View experiments, metrics, and model registry |
| API Docs | http://localhost:8001/docs | Interactive API documentation (Swagger) |
| API Health | http://localhost:8001 | Health check endpoint |


### Interacting with the app
Once Docker Compose is running, you can connect to the various UIs to perform certain actions.

From the [Prefect UI](http://0.0.0.0:4200), you can see the deployed workflows, and launch one manually to check everything works (go to ```Deployments``` --> ```abalone-training-daily``` --> ```Run``` (located on top right) --> ```Quick Run```). This triggers the training workflow to run, and you can see the outputs of this on the [MLFlow UI](http://localhost:5000).

> **Note**: There is nothing to fetch new data in this app, so the retraining of the model is alwas performed on the same dataset that is in the Docker backend image. A next step could be to implement a way to retrieve new data and train the model on that data.

You can also predict the age of an abalone from the [Fast API UI](http://localhost:5000). Click on the ```/predict``` endpoint and on the ```Try it out``` button. You can modify the request body of the API call, and visualize the results in the ```Responses``` section after clicking on the ```Execute``` button.

### Stopping the app
Simply run in your terminal:
```zsh
docker compose down
```
