FROM python:3.12-slim

WORKDIR /app

# Install build tools needed by some usdm dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency spec first for layer caching
COPY pyproject.toml .

# Install runtime dependencies only (no dev extras in the image)
RUN pip install --no-cache-dir ".[" 2>/dev/null || pip install --no-cache-dir \
    "fastapi[standard]>=0.115.0" \
    "motor>=3.6.0" \
    "pymongo>=4.10.0" \
    "pydantic>=2.10.0" \
    "pydantic-settings>=2.7.0" \
    "usdm==0.67.0"

# Copy application source
COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
