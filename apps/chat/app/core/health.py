from fastapi import APIRouter

import structlog
from app.logger import enrich_context

health_router = APIRouter(prefix="/health", tags=["health"])

@health_router.get("", summary="Health check", response_model=dict)
async def health():
    """
    Healthcheck endpoint для мониторинга и Kubernetes/LB.
    """
    structlog.get_logger("chat").bind(
        **enrich_context(event="health_check")
    ).info("Health check called")
    return {"status": "ok"}
