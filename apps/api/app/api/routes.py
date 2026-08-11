from uuid import uuid4
from fastapi import APIRouter, HTTPException
from app.schemas.generation import GenerateRequest, GenerateResponse
from app.services.generator import generate_project, list_templates, export_project

router = APIRouter()

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

@router.get("/projects/{project_id}")
def project(project_id: str):
    raise HTTPException(status_code=501, detail="Project persistence will be enabled in the next persistence milestone")

@router.post("/export/{project_id}")
def export(project_id: str):
    try:
        return export_project(project_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
