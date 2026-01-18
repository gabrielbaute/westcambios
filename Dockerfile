# --- Stage 1: Builder ---
FROM python:3.12-slim as builder

WORKDIR /build

# Dependencias para compilar librerías de C (bcrypt/cryptography)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY pyproject.toml ./
# Configuramos poetry para que no cree entornos virtuales dentro del contenedor
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root --only main --compile && \
    # Movemos las librerías instaladas a una carpeta para el stage final
    mkdir -p /install && cp -R /usr/local/* /install/

# --- Stage 2: Final Runtime ---
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

# Crear usuario y grupos con el rigor de seguridad necesario
RUN groupadd -g 1000 westgroup && \
    useradd -u 1000 -g westgroup -m -s /bin/bash westuser

# Copiamos las dependencias del builder
COPY --from=builder /install /usr/local

# Copiamos el código y los estáticos
COPY ./app ./app
#COPY ./static ./static

# Creamos los directorios que Config espera y damos permisos
# Esto es crítico para evitar errores de escritura en Docker
RUN mkdir -p instance logs uploads && \
    chown -R westuser:westgroup /app

USER westuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]