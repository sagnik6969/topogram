# Stage 1: Generate requirements.txt
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS requirements-stage

WORKDIR /tmp

COPY pyproject.toml uv.lock ./

RUN uv export --frozen --no-dev --format requirements-txt > requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy requirements.txt from requirements-stage
COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application code
COPY app app/


# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
