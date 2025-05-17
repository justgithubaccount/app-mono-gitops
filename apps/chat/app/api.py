from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from .schemas import ChatRequest, ChatResponse, Message
from .services.chat_service import ChatService

api_router = APIRouter(
    prefix="/api/v1",
    tags=["chat"]
)

# Dependency — chat service (можно мокать и расширять)
def get_chat_service():
    return ChatService()

@api_router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить ответ от LLM"
)
async def chat_endpoint(
    req: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Асинхронно получить ответ от AI/LLM на список сообщений.
    """
    try:
        reply = await chat_service.get_ai_reply(req.messages)
        return ChatResponse(reply=reply)
    except Exception as e:
        # Можно добавить кастомный exception handler для разных ошибок
        raise HTTPException(status_code=500, detail="AI сервис недоступен")
