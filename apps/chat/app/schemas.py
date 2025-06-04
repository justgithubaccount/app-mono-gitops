from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from uuid import uuid4


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
    messages: List[Message] = Field(..., alias="messages", example=[{"role": "user", "content": "Hi"}])
    user_api_key: Optional[str] = Field(
        default=None,
        alias="userApiKey",
        example="sk-my-key"
    )

    class Config:
        populate_by_name = True

class ChatResponse(BaseModel):
    reply: str = Field(..., example="Hello, world")

# ----------------------------------------
# 📂 Память и проекты
# ----------------------------------------



class CreateProjectRequest(BaseModel):
    name: str = Field(..., example="My Project")

class ProjectInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), example="123e4567-e89b-12d3-a456-426614174000")
    name: str = Field(..., example="My Project")
