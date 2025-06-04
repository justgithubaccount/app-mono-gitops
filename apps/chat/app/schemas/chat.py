from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional


# ----------------------------------------
# 📌 Роли сообщений
# ----------------------------------------
class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

# ----------------------------------------
# 📌 Базовое сообщение
# ----------------------------------------
class Message(BaseModel):
    role: Role = Field(..., example="user")
    content: str = Field(..., example="Hello")

# ----------------------------------------
# 📌 Структура запроса и ответа чата
# ----------------------------------------
class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., example=[{"role": "user", "content": "Hi"}])
    user_api_key: Optional[str] = Field(None, alias="userApiKey", example="sk-...")

    class Config:
        allow_population_by_field_name = True

class ChatResponse(BaseModel):
    reply: str = Field(..., example="Hello from AI")

