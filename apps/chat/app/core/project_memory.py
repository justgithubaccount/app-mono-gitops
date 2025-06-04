from typing import Dict, List
from app.schemas import ProjectInfo, CreateProjectRequest, ChatHistory, ChatMessage
from uuid import uuid4
from datetime import datetime

from app.logger import with_context

class ProjectMemory:
    def __init__(self):
        self.projects: Dict[str, ProjectInfo] = {}
        self.histories: Dict[str, List[ChatHistory]] = {}
        with_context(event="memory_init").info("Project memory initialized")

    def create_project(self, name: str) -> ProjectInfo:
        project_id = str(uuid4())
        project = ProjectInfo(id=project_id, name=name)
        self.projects[project_id] = project
        self.histories[project_id] = []
        with_context(
            event="project_created", project_id=project_id, project_name=name
        ).info("Project created in memory")
        return project

    def list_projects(self) -> List[ProjectInfo]:
        with_context(event="projects_listed", count=len(self.projects)).info(
            "Listing projects"
        )
        return list(self.projects.values())

    def add_chat(self, project_id: str, messages: List[ChatMessage]) -> ChatHistory:
        if project_id not in self.projects:
            with_context(event="project_not_found", project_id=project_id).warning(
                "Attempt to add chat to missing project"
            )
            raise ValueError(f"Проект {project_id} не найден")
        history = ChatHistory(project_id=project_id, messages=messages)
        self.histories[project_id].append(history)
        with_context(event="chat_saved", project_id=project_id).info(
            "Chat added to project"
        )
        return history

    def get_project_history(self, project_id: str) -> List[ChatHistory]:
        if project_id not in self.projects:
            with_context(event="project_not_found", project_id=project_id).warning(
                "History requested for missing project"
            )
            raise ValueError(f"Проект {project_id} не найден")
        with_context(event="history_retrieved", project_id=project_id).info(
            "Returning project history"
        )
        return self.histories.get(project_id, [])
