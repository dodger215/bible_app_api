FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy application files
COPY pyproject.toml /app/pyproject.toml
COPY app /app/app
COPY source /app/source
COPY .env /app/.env

# Install system build deps for packages like lxml
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libxml2-dev libxslt1-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Install runtime dependencies (mirrors pyproject.toml)
RUN pip install --no-cache-dir \
    "dotenv>=0.9.9" \
    "fastapi[all]>=0.138.0" \
    "google-genai>=2.9.0" \
    "google-generativeai>=0.8.6" \
    "lxml>=6.1.1" \
    "uvicorn>=0.49.0"

EXPOSE 8000

# Default command to run the app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
