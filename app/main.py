import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from sqlalchemy import text
from starlette.requests import Request
import asyncio
import httpx
import smtplib
from email.message import EmailMessage

from .db import get_engine, get_session

from datetime import datetime

app = FastAPI(title="Uptime Monitor", version="1.0.0")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
templates.env.globals["now"] = datetime.utcnow 

engine = get_engine()
security = HTTPBasic()

# --- Email Notification Function ---
def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_FROM")
    msg["To"] = to_email
    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.send_message(msg)

# --- Simple HTTP Basic Auth for dashboard ---
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("ADMIN_USER", "admin")
    correct_password = os.getenv("ADMIN_PASS", "password")
    if (
        credentials.username != correct_username
        or credentials.password != correct_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- Background Monitoring Task with Notifications ---
async def check_monitors_periodically():
    last_status = {}
    while True:
        with get_session() as session:
            monitors = session.execute(
                text("SELECT id, name, url FROM monitors")
            ).mappings().all()
        for monitor in monitors:
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    resp = await client.get(monitor["url"])
                    status = "up" if resp.status_code == 200 else "down"
            except Exception:
                status = "down"
            # Send notification if status changed
            if monitor["id"] not in last_status or last_status[monitor["id"]] != status:
                if status == "down":
                    send_email(
                        subject=f"Monitor DOWN: {monitor['name']}",
                        body=f"{monitor['url']} is DOWN.",
                        to_email=os.getenv("ALERT_EMAIL"),
                    )
                elif status == "up" and last_status.get(monitor["id"]) == "down":
                    send_email(
                        subject=f"Monitor UP: {monitor['name']}",
                        body=f"{monitor['url']} is back UP.",
                        to_email=os.getenv("ALERT_EMAIL"),
                    )
            last_status[monitor["id"]] = status
            with get_session() as session:
                session.execute(
                    text(
                        "UPDATE monitors SET status=:status, last_checked=:last_checked WHERE id=:id"
                    ),
                    {
                        "status": status,
                        "last_checked": datetime.utcnow(),
                        "id": monitor["id"],
                    },
                )
        await asyncio.sleep(60)  # Check every 60 seconds

@app.on_event("startup")
async def start_monitoring():
    asyncio.create_task(check_monitors_periodically())

# --- Database Initialization ---
@app.on_event("startup")
def init_db():
    ddl_sqlite = """
    CREATE TABLE IF NOT EXISTS monitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        interval_seconds INTEGER NOT NULL DEFAULT 60,
        status TEXT DEFAULT 'pending',
        last_checked TIMESTAMP
    );
    """
    ddl_pg = """
    CREATE TABLE IF NOT EXISTS monitors (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        interval_seconds INTEGER NOT NULL DEFAULT 60,
        status TEXT DEFAULT 'pending',
        last_checked TIMESTAMP
    );
    """
    ddl = ddl_sqlite if engine.dialect.name == "sqlite" else ddl_pg
    with engine.begin() as conn:
        conn.execute(text(ddl))

# --- Pydantic Models ---
class MonitorCreate(BaseModel):
    name: str
    url: str
    interval_seconds: int = 60

class MonitorUpdate(BaseModel):
    name: str
    url: str
    interval_seconds: int = 60

# --- Routes ---
@app.get("/", response_class=HTMLResponse)
def ui_home(request: Request):
    with get_session() as session:
        monitors = session.execute(
            text(
                "SELECT id, name, url, interval_seconds, status, last_checked "
                "FROM monitors ORDER BY id DESC"
            )
        ).mappings().all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Uptime Monitor", "monitors": monitors},
    )

@app.get("/monitors")
def list_monitors():
    try:
        with get_session() as session:
            rows = session.execute(
                text(
                    "SELECT id, name, url, interval_seconds, status, last_checked "
                    "FROM monitors ORDER BY id DESC"
                )
            ).mappings().all()
        return list(rows)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/monitors/{monitor_id}")
def get_monitor(monitor_id: int):
    try:
        with get_session() as session:
            row = session.execute(
                text(
                    "SELECT id, name, url, interval_seconds, status, last_checked "
                    "FROM monitors WHERE id = :id"
                ),
                {"id": monitor_id},
            ).mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="Monitor not found")
        return row
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/monitors")
def create_monitor(payload: MonitorCreate):
    try:
        with get_session() as session:
            session.execute(
                text(
                    "INSERT INTO monitors (name, url, interval_seconds, status) "
                    "VALUES (:name, :url, :interval_seconds, 'pending')"
                ),
                {
                    "name": payload.name,
                    "url": payload.url,
                    "interval_seconds": payload.interval_seconds,
                },
            )
        return {"created": True}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.put("/monitors/{monitor_id}")
def update_monitor(monitor_id: int, payload: MonitorUpdate):
    try:
        with get_session() as session:
            result = session.execute(
                text(
                    "UPDATE monitors "
                    "SET name = :name, url = :url, interval_seconds = :interval_seconds "
                    "WHERE id = :id"
                ),
                {
                    "id": monitor_id,
                    "name": payload.name,
                    "url": payload.url,
                    "interval_seconds": payload.interval_seconds,
                },
            )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Monitor not found")
        return {"updated": True}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.delete("/monitors/{monitor_id}")
def delete_monitor(monitor_id: int):
    try:
        with get_session() as session:
            result = session.execute(
                text("DELETE FROM monitors WHERE id = :id"),
                {"id": monitor_id},
            )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Monitor not found")
        return {"deleted": True}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))