from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["health"])

@health_router.get("", summary="Health check", response_model=dict)
async def health():
    """
    Healthcheck endpoint для мониторинга и Kubernetes/LB.
    """
    return {"status": "ok"}
