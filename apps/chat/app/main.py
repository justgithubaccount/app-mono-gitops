from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router
from .core.health import health_router

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

    @app.get("/")
    async def root():
        return {
            "status": "ok",
            "service": app.title,
            "version": app.version
        }

    return app

app = create_app()
