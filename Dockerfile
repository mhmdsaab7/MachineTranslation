# ---- Base image ----
FROM python:3.11-slim

# Keep Python from writing .pyc files & make logs unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TF_CPP_MIN_LOG_LEVEL=2

# System deps (build tools often needed by TF / numpy wheels)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt /app/

# TIP: If you don’t need GPU, prefer tensorflow-cpu in requirements.txt to keep image smaller.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the project
# Make sure your tree looks like:
# app.py, mt/, models/artifacts/, templates/, static/
COPY . /app


# Gunicorn will serve the Flask app
EXPOSE 7860
CMD ["gunicorn", "-w", "2", "-k", "gthread", "-b", "0.0.0.0:7860", "app:app"]
