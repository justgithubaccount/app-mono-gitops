# apps/chat/app/models/chat.py
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from ..schemas import Role


class StoredChatMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    role: Role
    content: str
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatHistory(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(default_factory=lambda: str(uuid4()))
    project_id: str
    messages: List[StoredChatMessage]
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# apps/chat/app/schemas/chat.py
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import List, Optional


class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Message(BaseModel):
    role: Role = Field(..., example="user")
    content: str = Field(..., example="Hello")


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    messages: List[Message] = Field(..., example=[{"role": "user", "content": "Hi"}])
    user_api_key: Optional[str] = Field(None, alias="userApiKey", example="sk-...")


class ChatResponse(BaseModel):
    reply: str = Field(..., example="Hello from AI")


# apps/chat/app/schemas/projects.py
from pydantic import BaseModel, Field


class CreateProjectRequest(BaseModel):
    name: str = Field(..., example="My Project")


class ProjectInfo(BaseModel):
    id: str = Field(..., example="project-123")
    name: str = Field(..., example="Demo Project")