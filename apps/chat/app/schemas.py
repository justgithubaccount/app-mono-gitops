from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

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
    role: Role
    content: str

# ----------------------------------------
# 📌 Структура запроса и ответа чата
# ----------------------------------------
class ChatRequest(BaseModel):
    messages: List[Message]
    user_api_key: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

# ----------------------------------------
# 📂 Память и проекты
# ----------------------------------------

class ChatMessage(BaseModel):
    role: Role
    content: str

class ChatHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    project_id: str
    messages: List[ChatMessage]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CreateProjectRequest(BaseModel):
    name: str

class ProjectInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
