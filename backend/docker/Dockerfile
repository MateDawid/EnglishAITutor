FROM python:3.14-slim AS base-image

ARG DEV="false"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \ 
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies

RUN if [ "$DEV" = "true" ]; then \
        uv pip install --system . --group dev; \
    else \
        uv pip install --system .; \
    fi

# Copy application code
COPY ./src /app/src

# Create user
RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app && \
    mkdir -p /app/src/staticfiles && chown -R app:app /app/src

# Copy entrypoint script and make it executable
COPY ./docker/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh  \
    && chmod +x /entrypoint.sh

# Test image
FROM base-image AS test-image

COPY ruff.toml ./
COPY ./tests /app/tests

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Release image
FROM base-image AS release-image

WORKDIR /app/src

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
