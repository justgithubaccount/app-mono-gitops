from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class TaskSchema(BaseModel):
    """Single task definition executed by an agent."""

    description: str = Field(..., example="Collect articles about AI")
    expected_output: Optional[str] = Field(
        None,
        alias="expected_output",
        example="List of article URLs",
    )
    context: Optional[List[str]] = Field(
        default_factory=list,
        example=["Use only academic sources"],
    )
    agent: Optional[str] = Field(None, example="researcher")

    model_config = ConfigDict(populate_by_name=True)


class AgentSchema(BaseModel):
    """CrewAI-style agent configuration."""

    role: str = Field(..., example="researcher")
    goal: Optional[str] = Field(None, example="Provide an overview of AI trends")
    backstory: Optional[str] = Field(None, example="PhD in computer science")
    tools: List[str] = Field(default_factory=list, example=["browser"])
    allow_delegation: bool = Field(False, alias="allow_delegation", example=True)
    tasks: List[TaskSchema] = Field(default_factory=list)

    model_config = ConfigDict(populate_by_name=True)


class BehaviorDefinition(BaseModel):
    """Root object describing agent behaviors loaded from Notion."""

    agents: List[AgentSchema] = Field(
        default_factory=list,
        example=[{"role": "researcher", "goal": "Find info"}],
    )
    tasks: List[TaskSchema] = Field(default_factory=list)
    process: Optional[str] = Field("sequential", example="sequential")

    model_config = ConfigDict(populate_by_name=True)
