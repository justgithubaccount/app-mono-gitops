from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api_router
from .core.health import health_router
from .observability.tracing import setup_tracing
from .logger import enrich_context
from .core.config import get_settings
from .core.db import init_db
from .integrations.notion_client import NotionClient
from .integrations.behavior_manager import BehaviorManager

from crewai import Crew
import os

def create_app() -> FastAPI:
    app = FastAPI(
        title="Chat Microservice",
        version="0.1.0"
    )

    settings = get_settings()

    @app.on_event("startup")
    def _init_db() -> None:
        init_db()

    if settings.notion_token and settings.notion_page_id:
        notion_client = NotionClient(settings.notion_token)
        behavior_manager = BehaviorManager(notion_client, settings.notion_page_id)
        app.state.behavior_manager = behavior_manager

        @app.on_event("startup")
        async def load_behavior():
            await behavior_manager.refresh()

    # CrewAI YAML
    @app.on_event("startup")
    async def load_crew():
        yaml_path = os.path.join(os.path.dirname(__file__), "infra_cluster.yaml")
        if os.path.exists(yaml_path):
            app.state.crew = Crew.load(yaml_path)
            enrich_context(event="crew_loaded", file=yaml_path).info("Crew loaded from YAML")
            # app.state.crew.kickoff()  # автостарт агентов

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Роуты
    app.include_router(api_router)
    app.include_router(health_router)

    # Трейсинг и лог старта
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
