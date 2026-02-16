# Uptime Monitor — FastAPI, PostgreSQL, Docker

## About This Project

This is a **production-ready uptime monitoring dashboard** built with FastAPI, PostgreSQL, Docker, and modern CI/CD practices.  
It features a real-time dashboard, background health checks, email notifications, and a clean, responsive UI.

**Why me?**  

- I design, build, and deploy robust, scalable backend systems.
- I automate everything: from Dockerized local dev to CI/CD pipelines.
- I write clean, well-documented code and deliver real business value.

---

## Key Features

- **FastAPI** backend with async health checks and RESTful API.
- **PostgreSQL** for reliable, transactional data storage.
- **Docker Compose** for reproducible, multi-container local and cloud deployments.
- **Nginx** reverse proxy for production-grade serving.
- **Jinja2** dashboard with live status, add-monitor form, and auto-refresh.
- **Email notifications** for downtime alerts (SMTP integration).
- **GitHub Actions** for automated testing and deployment.
- **Security**: HTTP Basic Auth (optional), environment-based secrets.
- **Full inline code comments** for clarity and maintainability.

---

## Project Structure

- `app/main.py` — FastAPI app, background tasks, API endpoints, dashboard logic.
- `app/db.py` — SQLAlchemy DB connection/session helpers.
- `app/models.py` — Table schema (ORM or raw SQL).
- `app/init_db.py` — DB initialization/migration script.
- `app/templates/index.html` — Responsive dashboard UI (Jinja2).
- `requirements.txt` — Python dependencies.
- `Dockerfile` — API container build.
- `docker-compose.yml` — Multi-container orchestration (API + Postgres + Nginx).
- `.github/workflows/ci.yml` — Automated CI/CD pipeline.

---

## How to Run

```bash
# 1. Build and start everything (API, DB, Nginx)
docker compose up --build

# 2. Access the dashboard
open http://localhost:8080  # or your VM's IP

# 3. Health check (API + DB)
curl http://localhost:8000/health

# 4. Add a monitor (example)
curl -X POST http://localhost:8000/monitors \
  -H "Content-Type: application/json" \
  -d '{"name":"example","url":"https://example.com","interval_seconds":60}'
```

---

## DevOps & CI/CD

- **GitHub Actions**: Runs tests, spins up Postgres, builds and deploys containers.
- **Docker Compose**: Ensures parity between local dev and production.
- **Environment Variables**: All secrets/configs are injected securely.

---

## Why I’m the Right Candidate

- **Fullstack DevOps**: I own the stack from Python backend to Docker, Nginx, and CI/CD.
- **Automation**: I automate builds, tests, and deployments for reliability and speed.
- **Clean Code**: My code is readable, maintainable, and well-commented.
- **Problem Solver**: I deliver solutions that work in production, not just in theory.
- **Team Player**: I document, communicate, and collaborate effectively.

---

**Let’s build reliable, scalable systems together!**
