from uuid import uuid4
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.blueprints.compiler import BlueprintCompiler
from app.schemas.generation import GenerateRequest, GenerateResponse
from app.services.generator import generate_project, list_templates, export_project

router = APIRouter()
blueprint_compiler = BlueprintCompiler()


class BlueprintRequest(BaseModel):
    project_name: str = Field(min_length=2, max_length=100)
    prompt: str = Field(min_length=3, max_length=10000)
    target_platforms: list[str] = Field(default_factory=lambda: ["web"], min_length=1, max_length=5)
    preferred_stack: dict[str, str] = Field(default_factory=dict)


@router.get("/templates")
def templates() -> list[dict[str, str]]:
    return list_templates()


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        project = generate_project(request)
        return GenerateResponse(**project)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/api/v1/blueprints")
def create_blueprint(request: BlueprintRequest) -> dict[str, Any]:
    try:
        blueprint, validation = blueprint_compiler.compile(
            prompt=request.prompt,
            project_name=request.project_name,
            target_platforms=request.target_platforms,
            preferred_stack=request.preferred_stack,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {
        "status": "draft",
        "blueprint": blueprint.model_dump(mode="json"),
        "validation": validation,
        "next_action": "Review and approve the blueprint before code generation.",
    }


@router.get("/projects/{project_id}")
def project(project_id: str):
    raise HTTPException(status_code=501, detail="Project persistence will be enabled in the next persistence milestone")


@router.post("/export/{project_id}")
def export(project_id: str):
    try:
        return export_project(project_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
