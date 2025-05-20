from fastapi import APIRouter, HTTPException, status, Depends
from .schemas import ChatRequest, ChatResponse
from .services.chat_service import ChatService

api_router = APIRouter(
    prefix="/api/v1",
    tags=["chat"]
)

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
        reply = await chat_service.get_ai_reply(req.messages, req.user_api_key)
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI сервис недоступен")
