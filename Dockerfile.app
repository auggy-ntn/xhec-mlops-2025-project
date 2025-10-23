# 1. Utiliser une image de base officielle qui contient Python 3.11 et uv
# cf doc astral : https://docs.astral.sh/uv/guides/integration/docker/#caching
# En gros c'est plus malin d'utiliser une image préfaite avec python et uv que
# de tout recréer from scratch.
FROM ghcr.io/astral-sh/uv:python3.11-slim-bookworm

WORKDIR /app_home

# 2. Copier uniquement les fichiers de dépendances
COPY pyproject.toml uv.lock /app_home/

# 3. Installer les dépendances (sans le projet)
# Ceci crée une couche Docker "lente" qui change rarement.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# 4. Copier le code source de l'application
COPY ./src /app_home/src

# 5. Installer le projet lui-même
# Cette couche est rapide car les dépendances sont déjà là.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# 6. Copier le script de démarrage et le rendre exécutable
COPY ./bin/run_services.sh /app_home/run_services.sh
RUN chmod +x /app_home/run_services.sh

# 7. Exposer les ports
EXPOSE 8001 4201

# 8. Lancer l'application, et ce pour les deux services mentionnés dans run_services.sh
CMD ["/app_home/run_services.sh"]
# 7. Lancer l'application
# Make sure to check bin/run_services.sh, which can be used here
