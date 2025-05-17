from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Конфиг всего приложения.
    Все переменные тянутся из .env — легко расширять и объяснять новым людям.
    """
    openai_api_key: str = ""
    llm_api_url: str = "http://localhost:4000"
    chat_model: str = "openai/gpt-4o"
    project_name: str = "ChatMicroservice"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()
