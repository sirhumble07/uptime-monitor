# Uptime Monitor APP

A robust, production-ready uptime monitoring dashboard built with **FastAPI**, **PostgreSQL**, **Docker**, and **Nginx**—fully automated with CI/CD on GitHub Actions.  
Designed for reliability, scalability, and developer productivity.

---

## Skills

- **Fullstack DevOps:** I design, build, and deploy end-to-end solutions—from backend APIs to Docker, Nginx, and CI/CD automation.
- **Automation First:** I automate builds, tests, and deployments for speed and reliability.
- **Clean, Maintainable Code:** My code is readable, well-documented, and production-focused.
- **Problem Solver:** I deliver solutions that work in real-world environments, not just in theory.
- **Team Player:** I communicate clearly and document everything for seamless collaboration.

---

## Features

- **FastAPI** backend with async health checks and RESTful CRUD API for monitors.
- **Jinja2** HTML dashboard UI with live status, add-monitor form, and auto-refresh.
- **PostgreSQL** (or SQLite) for reliable data storage.
- **Dockerized** for easy, reproducible deployment.
- **Nginx** reverse proxy for secure, production-grade serving.
- **Email notifications** for downtime alerts (SMTP integration).
- **GitHub Actions** workflow for automated CI/CD (self-hosted runner ready).
- **Live health/status endpoints** for monitoring and alerting.
- **Environment-based secrets** for security.

---

## Quick Start (Local)

1. **Clone the repo**

    ```bash
    git clone https://github.com/sirhumble07/uptime-monitor.git
    cd uptime-monitor
    ```

2. **Build and run with Docker Compose**

    ```bash
    docker compose up --build
    ```

3. **Open the app**
    - Dashboard: [http://localhost:8080/](http://localhost:8080/)
    - Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

## Deployment (Production)

### 1. **Push to GitHub**

- Commit and push your code to your GitHub repository.

### 2. **Set up your Linux VM or cloud server**

- Install Docker, Docker Compose, and Nginx.
- Register a GitHub Actions self-hosted runner on your VM.

### 3. **Configure Nginx**

- Use the provided `nginx/uptime-monitor.conf` as a reverse proxy (port 8080 or 80).
- (Optional) Set up HTTPS with Certbot for SSL.

### 4. **CI/CD**

- On every push to `main`, GitHub Actions will build and deploy your app using Docker Compose on your VM.

---

## File Structure

```text
uptime-monitor/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── static/
│   │   ├── app.js
│   │   ├── styles.css
│   │   └── favicon.svg
│   └── templates/
│       └── index.html
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── nginx/
│   └── uptime-monitor.conf
├── .github/
│   └── workflows/
│       └── deploy.yml
└── README.md
```

---

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (e.g. `postgresql+psycopg2://app:app@localhost/uptime`)
- `ADMIN_USER`, `ADMIN_PASS`: Dashboard authentication (optional, can be disabled)
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`, `ALERT_EMAIL`: For email notifications

---

## License

MIT

---

**Let’s build reliable, scalable systems together!**
