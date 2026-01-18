"""
Module for defining the API health routes.
"""
from fastapi import APIRouter, status, HTTPException

from app.config import Config

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint to verify API is running."""
    return {
        "status": "OK",
        "message": "API is running",
        "service": "WestCambios API",
        "version": Config.APP_VERSION
        }