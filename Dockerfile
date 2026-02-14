# Use a slim Python base image for smaller size.
# Base image with Python.
FROM python:3.12-slim

# Set working directory inside the container.
# All commands run from here.
WORKDIR /app

# Copy dependency list first to leverage Docker layer cache.
# Copy requirements.txt for dependency installation.
COPY requirements.txt /app/  

# Install dependencies.
RUN pip install --no-cache-dir -r /app/requirements.txt  # Install Python packages.

# Copy the application code.
# Copy app package.
COPY app /app/app

# Set environment so Python treats /app as module root.
# Make app importable.
ENV PYTHONPATH=/app  

# Expose the default FastAPI port.
# Document container port.
EXPOSE 8000

# Run DB init and start the server.
CMD ["/bin/sh", "-c", "python -m app.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]  # Initialize DB then start API.
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]