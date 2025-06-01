from typing import Dict, List
from app.schemas import ProjectInfo, CreateProjectRequest, ChatHistory, ChatMessage
from uuid import uuid4
from datetime import datetime

class ProjectMemory:
    def __init__(self):
        self.projects: Dict[str, ProjectInfo] = {}
        self.histories: Dict[str, List[ChatHistory]] = {}

    def create_project(self, name: str) -> ProjectInfo:
        project_id = str(uuid4())
        project = ProjectInfo(id=project_id, name=name)
        self.projects[project_id] = project
        self.histories[project_id] = []
        return project

    def list_projects(self) -> List[ProjectInfo]:
        return list(self.projects.values())

    def add_chat(self, project_id: str, messages: List[ChatMessage]) -> ChatHistory:
        if project_id not in self.projects:
            raise ValueError(f"Проект {project_id} не найден")
        history = ChatHistory(project_id=project_id, messages=messages)
        self.histories[project_id].append(history)
        return history

    def get_project_history(self, project_id: str) -> List[ChatHistory]:
        if project_id not in self.projects:
            raise ValueError(f"Проект {project_id} не найден")
        return self.histories.get(project_id, [])
