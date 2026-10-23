from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

ProjectType = Literal[
    "website", "ecommerce", "saas", "api", "dashboard", "mobile_app", "automation", "ai_app", "other"
]


class StackSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    frontend: str = "react-vite"
    backend: str = "fastapi"
    database: str = "postgresql"
    deployment: str = "docker"


class RequirementSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^REQ-[0-9]{3}$")
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5, max_length=1000)
    priority: Literal["must", "should", "could"] = "must"
    acceptance_criteria: list[str] = Field(default_factory=list, min_length=1, max_length=10)


class ComponentSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=2, max_length=80)
    kind: Literal["frontend", "backend", "database", "integration", "infrastructure", "worker"]
    responsibilities: list[str] = Field(default_factory=list, max_length=12)
    depends_on: list[str] = Field(default_factory=list, max_length=20)


class ProjectBlueprint(BaseModel):
    """Versioned, typed contract shared by planning and generation stages."""
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal["1.0"] = "1.0"
    project_name: str = Field(min_length=2, max_length=100)
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=100)
    project_type: ProjectType = "website"
    prompt: str = Field(min_length=3, max_length=10000)
    target_platforms: list[str] = Field(default_factory=lambda: ["web"], min_length=1, max_length=5)
    stack: StackSpec = Field(default_factory=StackSpec)
    requirements: list[RequirementSpec] = Field(default_factory=list, min_length=1, max_length=100)
    components: list[ComponentSpec] = Field(default_factory=list, min_length=1, max_length=50)
    security_requirements: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("target_platforms")
    @classmethod
    def normalize_platforms(cls, values: list[str]) -> list[str]:
        normalized = list(dict.fromkeys(v.strip().lower() for v in values if v.strip()))
        if not normalized:
            raise ValueError("At least one target platform is required")
        return normalized
