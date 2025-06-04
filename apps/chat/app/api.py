from fastapi import APIRouter, HTTPException, status, Depends
from .schemas import (
    ChatRequest, ChatResponse, Message,
    CreateProjectRequest, ProjectInfo,
)
from .models import ChatHistory, StoredChatMessage
from .services.chat_service import ChatService
from .core.project_memory import ProjectMemory
import structlog
from app.logger import enrich_context
from opentelemetry import metrics

meter = metrics.get_meter(__name__)
chat_counter = meter.create_counter("chat_requests_total")
import traceback

api_router = APIRouter(
    prefix="/api/v1",
    tags=["chat"]
)

memory = ProjectMemory()

def get_chat_service():
    return ChatService()

@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    log = structlog.get_logger("chat").bind(
        **enrich_context(
            event="chat_api_called",
            endpoint="/chat",
            user_message=req.messages[-1].content if req.messages else None,
        )
    )
    chat_counter.add(1, {"project_id": "default"})

    log.info("Received standard chat request")

    try:
        reply = await chat_service.get_ai_reply(req.messages, req.user_api_key)
        return ChatResponse(reply=reply)

    except Exception as e:
        log.bind(event="chat_api_error", error=str(e)).error("Standard chat request failed")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="AI сервис недоступен")

@api_router.post("/projects", response_model=ProjectInfo)
def create_project(req: CreateProjectRequest):
    project = memory.create_project(req.name)
    structlog.get_logger("chat").bind(
        **enrich_context(
            event="project_created",
            project_id=project.id,
            project_name=project.name,
        )
    ).info("New project created")
    return project

@api_router.get("/projects", response_model=list[ProjectInfo])
def list_projects():
    structlog.get_logger("chat").bind(
        **enrich_context(event="project_list_requested")
    ).info("Project list requested")
    return memory.list_projects()

@api_router.post("/projects/{project_id}/chat", response_model=ChatResponse)
async def chat_in_project(
    project_id: str,
    req: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    log = structlog.get_logger("chat").bind(
        **enrich_context(
            event="project_chat_called",
            endpoint=f"/projects/{project_id}/chat",
            project_id=project_id,
            user_message=req.messages[-1].content if req.messages else None,
        )
    )
    chat_counter.add(1, {"project_id": project_id})

    log.info("Chat within project requested")

    try:
        chat_messages = [
            StoredChatMessage(role=m.role, content=m.content)
            for m in req.messages
        ]
        memory.add_chat(project_id, chat_messages)

        reply = await chat_service.get_ai_reply(
            req.messages, req.user_api_key, project_id=project_id
        )
        return ChatResponse(reply=reply)

    except ValueError as e:
        log.bind(event="project_not_found").warning("Project not found")
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        log.bind(event="project_chat_error", error=str(e)).error("Project chat failed")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Ошибка при обращении к AI")

@api_router.get("/projects/{project_id}/history", response_model=list[ChatHistory])
def get_project_history(project_id: str):
    log = structlog.get_logger("chat").bind(
        **enrich_context(event="project_history_requested", project_id=project_id)
    )

    log.info("Project history requested")

    try:
        return memory.get_project_history(project_id)
    except ValueError as e:
        log.bind(event="project_history_not_found").warning("Project not found when fetching history")
        raise HTTPException(status_code=404, detail=str(e))
