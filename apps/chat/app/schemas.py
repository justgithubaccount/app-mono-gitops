from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Message(BaseModel):
    role: Role = Field(..., description="Роль отправителя ('user', 'assistant', 'system')")
    content: str = Field(..., description="Текст сообщения")

    class Config:
        schema_extra = {
            "example": {
                "role": "user",
                "content": "Привет!"
            }
        }

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="История чата")

    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "Привет!"},
                    {"role": "assistant", "content": "Здравствуйте! Чем могу помочь?"}
                ]
            }
        }

class ChatResponse(BaseModel):
    reply: str = Field(..., description="Ответ LLM/AI")

    class Config:
        schema_extra = {
            "example": {
                "reply": "Здравствуйте! Чем могу помочь?"
            }
        }
