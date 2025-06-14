from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from .core.health import health_router
from .observability.tracing import setup_tracing
from .logger import enrich_context
from .core.config import get_settings
from .integrations.notion_client import NotionClient
from .integrations.behavior_manager import BehaviorManager

def create_app() -> FastAPI:
    app = FastAPI(
        title="Chat Microservice",
        version="0.1.0"
    )

    settings = get_settings()

    if settings.notion_token and settings.notion_page_id:
        notion_client = NotionClient(settings.notion_token)
        behavior_manager = BehaviorManager(notion_client, settings.notion_page_id)
        app.state.behavior_manager = behavior_manager

        @app.on_event("startup")
        async def load_behavior():
            await behavior_manager.refresh()

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
    enrich_context(event="startup").info("Application initialized")

    @app.get("/")
    async def root():
        enrich_context(event="root_called").info("Root endpoint accessed")
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
