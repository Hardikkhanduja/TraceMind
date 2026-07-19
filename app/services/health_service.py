from datetime import datetime,UTC


class HealthService:
    """
    Handles all business logic related to system health.
    """

    @staticmethod
    def get_health_status():
        return {
            "status": "healthy",
            "service": "TraceMind Backend",
            "timestamp": datetime.now(UTC).isoformat()
        }