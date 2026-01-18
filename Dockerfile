# --- Stage 1: Builder ---
FROM python:3.12-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*

    RUN pip install --no-cache-dir poetry    
    
    COPY pyproject.toml ./

    RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main --compile && \
    mkdir -p /install && cp -R /usr/local/* /install/

# --- Stage 2: Final Runtime ---
FROM python:3.12-slim

# Instalamos curl para el healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN groupadd -g 1000 westgroup && \
    useradd -u 1000 -g westgroup -m -s /bin/bash westuser

COPY --from=builder /install /usr/local

# COPIAR CÓDIGO Y ESTÁTICOS (Importante para el Admin Panel)
COPY ./app ./app

RUN mkdir -p instance logs uploads && \
    chown -R westuser:westgroup /app

# Argumentos para metadata (inyectados por GitHub Actions)
ARG BUILD_DATE
ARG VCS_REF
LABEL org.opencontainers.image.created=$BUILD_DATE \
      org.opencontainers.image.revision=$VCS_REF \
      org.opencontainers.image.authors="Gabriel Baute <gabrielbaute@gmail.com>"

USER westuser
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]