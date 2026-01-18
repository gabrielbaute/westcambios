# --- Stage 1: Builder ---
FROM python:3.12-slim as builder

WORKDIR /build

# Instalamos dependencias de compilación necesarias para bcrypt/cryptography
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalamos poetry para manejar las dependencias limpiamente
RUN pip install --no-cache-dir poetry

# Copiamos solo los archivos de configuración
COPY pyproject.toml ./

# Generamos un requirements.txt limpio desde poetry y lo instalamos en un directorio temporal
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Stage 2: Final Runtime ---
FROM python:3.12-slim

# Metadatos del proyecto
LABEL maintainer="Gabriel Baute <gabrielbaute@gmail.com>"
LABEL org.opencontainers.image.description="WestCambios Admin Panel & API"

# Variables de entorno para Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

WORKDIR /app

# Crear usuario no privilegiado (Seguridad: Principle of Least Privilege)
RUN groupadd -g 1000 westgroup && \
    useradd -u 1000 -g westgroup -m -s /bin/bash westuser

# Copiar solo las librerías instaladas desde el builder
COPY --from=builder /install /usr/local

# Copiar el código de la aplicación
COPY ./app ./app
COPY ./static ./static

# Asegurar permisos correctos para el usuario
RUN chown -R westuser:westgroup /app

USER westuser

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando de ejecución
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]