from fastapi import APIRouter

from app.logger import with_context

health_router = APIRouter(prefix="/health", tags=["health"])

@health_router.get("", summary="Health check", response_model=dict)
async def health():
    """
    Healthcheck endpoint для мониторинга и Kubernetes/LB.
    """
    with_context(event="health_check").info("Health check called")
    return {"status": "ok"}
