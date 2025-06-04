from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from .core.health import health_router
from .observability.tracing import setup_tracing
from .logger import with_context

def create_app() -> FastAPI:
    app = FastAPI(
        title="Chat Microservice",
        version="0.1.0"
    )
    # CORS: на проде настрой через ENV/config
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Внешние роутеры (можно делегировать)
    app.include_router(api_router)
    app.include_router(health_router)

    # Настраиваем OpenTelemetry и логируем запуск
    setup_tracing(app)
    with_context(event="startup").info("Application initialized")

    @app.get("/")
    async def root():
        with_context(event="root_called").info("Root endpoint accessed")
        return {
            "status": "ok",
            "service": app.title,
            "version": app.version
        }

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
