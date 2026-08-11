from fastapi import FastAPI
from pydantic import BaseModel, Field

from packages.orchestrator.orchestrator import ApplicationOrchestrator

app = FastAPI(title="AI Application Factory API", version="0.1.0")
orchestrator = ApplicationOrchestrator()


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=10000)
    project_name: str = Field(default="generated-app", min_length=1, max_length=100)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/generate")
def generate(request: GenerateRequest) -> dict:
    return orchestrator.run(request.prompt, request.project_name)
