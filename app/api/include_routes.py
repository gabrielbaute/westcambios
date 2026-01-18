"""
Helper to load all the api routes.
"""

from fastapi import FastAPI

from app.api.routes.health_routes import router as health_router
from app.api.routes.rates_routes import router as rates_router
from app.api.routes.admin_routes import router as admin_router
from app.api.routes.user_routes import router as user_router
from app.api.routes.auth_routes import router as auth_router

def include_routes(app: FastAPI, prefix: str):
    """Include all API routes in the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(auth_router, prefix=prefix, tags=["Authentication"])
    app.include_router(rates_router, prefix=prefix, tags=["Exchange Rates"])
    app.include_router(user_router, prefix=prefix, tags=["Users"])
    app.include_router(admin_router, prefix=prefix, tags=["Administration"])
    app.include_router(health_router, prefix=prefix, tags=["Health"])