from fastapi import APIRouter
from app.config.settings import settings

router = APIRouter(tags=["Health"])


@router.get("/", summary="Root status endpoint")
def root_endpoint():
    """Root welcome and version status."""
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "message": "CodeSense AI API is running successfully."
    }


@router.get("/health", summary="Health check endpoint")
def health_check():
    """Health check for service monitoring."""
    return {
        "status": "healthy",
        "openai_configured": bool(settings.OPENAI_API_KEY)
    }
