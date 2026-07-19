from fastapi import APIRouter

from app.services.health_service import HealthService

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return HealthService.get_health_status()