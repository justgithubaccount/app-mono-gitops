from typing import Dict, List
from app.schemas import ProjectInfo
from app.models import ChatHistory, StoredChatMessage
from uuid import uuid4

import structlog
from opentelemetry.trace import get_current_span
from app.logger import enrich_context

class ProjectMemory:
    def __init__(self):
        self.projects: Dict[str, ProjectInfo] = {}
        self.histories: Dict[str, List[ChatHistory]] = {}
        structlog.get_logger("chat").bind(
            **enrich_context(event="memory_init")
        ).info("Project memory initialized")

    def create_project(self, name: str) -> ProjectInfo:
        project_id = str(uuid4())
        project = ProjectInfo(id=project_id, name=name)
        self.projects[project_id] = project
        self.histories[project_id] = []
        structlog.get_logger("chat").bind(
            **enrich_context(
                event="project_created", project_id=project_id, project_name=name
            )
        ).info("Project created in memory")
        return project

    def list_projects(self) -> List[ProjectInfo]:
        structlog.get_logger("chat").bind(
            **enrich_context(event="projects_listed", count=len(self.projects))
        ).info("Listing projects")
        return list(self.projects.values())

    def add_chat(self, project_id: str, messages: List[StoredChatMessage]) -> ChatHistory:
        if project_id not in self.projects:
            structlog.get_logger("chat").bind(
                **enrich_context(event="project_not_found", project_id=project_id)
            ).warning("Attempt to add chat to missing project")
            raise ValueError(f"Проект {project_id} не найден")
        span = get_current_span()
        trace = span.get_span_context() if span else None
        history = ChatHistory(
            project_id=project_id,
            messages=messages,
            trace_id=format(trace.trace_id, "032x") if trace and trace.trace_id != 0 else None,
            span_id=format(trace.span_id, "016x") if trace and trace.trace_id != 0 else None,
        )
        self.histories[project_id].append(history)
        structlog.get_logger("chat").bind(
            **enrich_context(event="chat_saved", project_id=project_id)
        ).info("Chat added to project")
        return history

    def get_project_history(self, project_id: str) -> List[ChatHistory]:
        if project_id not in self.projects:
            structlog.get_logger("chat").bind(
                **enrich_context(event="project_not_found", project_id=project_id)
            ).warning("History requested for missing project")
            raise ValueError(f"Проект {project_id} не найден")
        structlog.get_logger("chat").bind(
            **enrich_context(event="history_retrieved", project_id=project_id)
        ).info("Returning project history")
        return self.histories.get(project_id, [])
