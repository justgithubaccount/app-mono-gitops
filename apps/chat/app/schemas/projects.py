from pydantic import BaseModel, Field

class CreateProjectRequest(BaseModel):
    name: str = Field(..., example="My Project")

class ProjectInfo(BaseModel):
    id: str = Field(..., example="project-123")
    name: str = Field(..., example="Demo Project")
