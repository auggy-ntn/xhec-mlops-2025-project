# 1. Use an official base image containing Python and uv
# see doc astral : https://docs.astral.sh/uv/guides/integration/docker/#caching
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app_home

# 2. Copy only the dependency files first
COPY pyproject.toml uv.lock /app_home/

# 3. Install dependencies (without the project)
# This layer is cached unless pyproject.toml or uv.lock change.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# 4. Copy the application source code
COPY ./src /app_home/src

# 5. Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# 6. Copy the startup script and make it executable
COPY ./bin/run_services.sh /app_home/run_services.sh
RUN chmod +x /app_home/run_services.sh

# 7. Expose the port that the FastAPI app will run on
EXPOSE 8001

# 8. Start the application, and this for the two services mentioned in run_services.sh
CMD ["/app_home/run_services.sh"]
# 7. Lancer l'application
# Make sure to check bin/run_services.sh, which can be used here
