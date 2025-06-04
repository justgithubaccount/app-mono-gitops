from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from .schemas import Role


class StoredChatMessage(BaseModel):
    role: Role = Field(..., example="user")
    content: str = Field(..., example="Hello")
    trace_id: Optional[str] = Field(None, example="9f1c...")
    span_id: Optional[str] = Field(None, example="a1b2...")
    timestamp: datetime = Field(default_factory=datetime.utcnow, example="2024-01-01T00:00:00Z")


class ChatHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), example="d4f0...")
    project_id: str = Field(..., alias="projectId", example="project-123")
    messages: List[StoredChatMessage]
    trace_id: Optional[str] = Field(None, alias="traceId", example="9f1c...")
    span_id: Optional[str] = Field(None, alias="spanId", example="a1b2...")
    timestamp: datetime = Field(default_factory=datetime.utcnow, example="2024-01-01T00:00:00Z")

    class Config:
        allow_population_by_field_name = True
