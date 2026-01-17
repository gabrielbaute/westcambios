"""
FastAPI Application Factory module
"""
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import Config
from app.api.include_routes import include_routes

def create_app(config: Config) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=config.APP_NAME,
        description="WestCambios API",
        version=config.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=Config.API_ALLOW_ORIGINS,
        allow_credentials=Config.API_ALLOW_CREDENTIALS,
        allow_methods=Config.API_ALLOW_METHODS,
        allow_headers=Config.API_ALLOW_HEADERS,
    )

    include_routes(app, prefix="/api/v1")

    return app