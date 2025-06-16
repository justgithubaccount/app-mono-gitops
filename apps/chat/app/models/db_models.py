from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Project(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str

class ChatHistoryDB(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    project_id: str = Field(foreign_key="project.id")
    messages: str
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

