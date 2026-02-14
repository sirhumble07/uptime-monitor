
import os  # Import os for environment variable access.
from datetime import datetime  # Import datetime for timestamping.
from fastapi import FastAPI, HTTPException  # Import FastAPI and HTTPException.
from fastapi.responses import HTMLResponse  # Import HTMLResponse for returning HTML content.
from fastapi.staticfiles import StaticFiles  # Import StaticFiles to serve static content.
from fastapi.templating import Jinja2Templates  # Import Jinja2Templates for rendering HTML templates.
from pydantic import BaseModel  # Import BaseModel to define request/response schemas.
from sqlalchemy import text  # Import text to run SQL.
from starlette.requests import Request  # Import Request for handling incoming HTTP requests.

from .db import get_engine, get_session  # Import helpers to connect to the database.

app = FastAPI(title="Uptime Monitor", version="1.0.0")  # Create the FastAPI app with metadata.

app.mount("/static", StaticFiles(directory="app/static"), name="static") # Mount the static files directory to serve CSS/JS/images.
templates = Jinja2Templates(directory="app/templates") # Set up Jinja2 templates directory for rendering HTML pages.
templates.env.globals["now"] = datetime.utcnow # Add a global function to templates to get the current UTC time.

engine = get_engine()  # Create the SQLAlchemy engine once at startup.



class MonitorCreate(BaseModel):
    name: str
    url: str
    interval_seconds: int = 60

class MonitorUpdate(BaseModel):
    name: str
    url: str
    interval_seconds: int = 60

@app.on_event("startup")
def init_db():
    ddl_sqlite = """
    CREATE TABLE IF NOT EXISTS monitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        interval_seconds INTEGER NOT NULL DEFAULT 60
    );
    """
    ddl_pg = """
    CREATE TABLE IF NOT EXISTS monitors (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        interval_seconds INTEGER NOT NULL DEFAULT 60
    );
    """
    ddl = ddl_sqlite if engine.dialect.name == "sqlite" else ddl_pg
    with engine.begin() as conn:
        conn.execute(text(ddl))

@app.get("/", response_class=HTMLResponse)
def ui_home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "Uptime Monitor"},
    )

@app.get("/monitors")
def list_monitors():
    try:
        with get_session() as session:
            rows = session.execute(
                text(
                    "SELECT id, name, url, interval_seconds "
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
                    "SELECT id, name, url, interval_seconds "
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
                    "INSERT INTO monitors (name, url, interval_seconds) "
                    "VALUES (:name, :url, :interval_seconds)"
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