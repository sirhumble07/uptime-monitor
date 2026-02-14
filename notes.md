# Notes

## Overview

- This project is a minimal FastAPI uptime monitor API with PostgreSQL running in Docker.
- Every file includes inline comments explaining each line.

## Files

- [app/main.py](app/main.py) — API endpoints and health checks.
- [app/db.py](app/db.py) — Database connection and session utilities.
- [app/models.py](app/models.py) — Table schema definitions.
- [app/init_db.py](app/init_db.py) — Database initialization script.
- [requirements.txt](requirements.txt) — Python dependencies.
- [Dockerfile](Dockerfile) — Container build steps.
- [docker-compose.yml](docker-compose.yml) — Local multi-container setup.
- [.github/workflows/ci.yml](.github/workflows/ci.yml) — GitHub Actions pipeline.

## Commands (with explanations)

1. docker compose up --build
   - Builds the API container from the Dockerfile.
   - Starts PostgreSQL and the API together.
   - Initializes the database schema automatically on container start.

2. curl [http://localhost:8000/health](http://localhost:8000/health)
   - Calls the health endpoint to verify the API and DB are reachable.

3. curl -X POST [http://localhost:8000/monitors](http://localhost:8000/monitors) -H "Content-Type: application/json" -d '{"name":"example","url":"https://example.com","interval_seconds":60}'
   - Creates a monitor record in the database.

## GitHub Actions

- The workflow spins up Postgres as a service container.
- It installs Python dependencies, initializes the DB, and runs a placeholder test.
