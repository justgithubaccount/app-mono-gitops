from __future__ import annotations

from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from .schemas import Role

class StoredChatMessage(BaseModel):
    role: Role
    content: str
    trace_id: Optional[str] = Field(default=None, example="97f5...")
    span_id: Optional[str] = Field(default=None, example="6b1f...")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    project_id: str
    messages: List[StoredChatMessage]
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
