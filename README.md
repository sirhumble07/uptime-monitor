# Uptime Monitor

A minimal, production-ready FastAPI uptime monitoring dashboard with Docker, CI/CD, and Nginx reverse proxy.

---

## Features

- FastAPI backend with CRUD for monitors
- Jinja2 HTML dashboard UI
- SQLite (default) or PostgreSQL support
- Dockerized for easy deployment
- GitHub Actions workflow for CI/CD (self-hosted runner)
- Nginx reverse proxy ready
- Live health/status endpoints

---

## Quick Start (Local)

1. **Clone the repo**

    ```bash
    git clone https://github.com/YOUR_USERNAME/uptime-monitor.git
    cd uptime-monitor
    ```

2. **Build and run with Docker Compose**

    ```bash
    docker compose up --build
    ```

3. **Open the app**
    - Dashboard: [http://localhost:8000/](http://localhost:8000/)
    - Health check: [http://localhost:8000/health](http://localhost:8000/health)

---

## Deployment (Production)

### 1. **Push to GitHub**

- Commit and push your code to your GitHub repository.

### 2. **Set up your Azure VM**

- Install Docker, Docker Compose, and Nginx.
- Register a GitHub Actions self-hosted runner on your VM.

### 3. **Configure Nginx**

- Use the provided `nginx/uptime-monitor.conf` as a reverse proxy.
- (Optional) Set up HTTPS with Certbot.

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

- `DATABASE_URL` (optional): Set to use PostgreSQL instead of SQLite.

---

## License

MIT
