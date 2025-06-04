from pydantic_settings import BaseSettings
from functools import lru_cache
import os

from app.logger import with_context

class Settings(BaseSettings):
    """
    Конфиг всего приложения.
    Все переменные тянутся из .env — легко расширять и объяснять новым людям.
    """
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_api_url: str = "http://localhost:4000"
    chat_model: str = "openai/gpt-4.1"
    project_name: str = "ChatMicroservice"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    settings = Settings()
    with_context(event="config_loaded").info("Settings loaded")
    return settings
