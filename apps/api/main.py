from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from packages.generator.artifact import Artifact
from packages.orchestrator.orchestrator import ApplicationOrchestrator

app = FastAPI(title="AI Application Factory API", version="0.2.0")
orchestrator = ApplicationOrchestrator()


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=10000)
    project_name: str = Field(default="generated-app", min_length=1, max_length=100)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/generate")
def generate(request: GenerateRequest) -> dict:
    result = orchestrator.run(request.prompt, request.project_name)
    if result["status"] != "generated":
        raise HTTPException(status_code=422, detail=result)
    return result


@app.post("/api/v1/generate/artifact")
def generate_artifact(request: GenerateRequest) -> Response:
    result = orchestrator.run(request.prompt, request.project_name)
    if result["status"] != "generated":
        raise HTTPException(status_code=422, detail=result)

    artifact = Artifact(result["project"], result["files"])
    filename = f"{request.project_name.replace('/', '-')}.zip"
    return Response(
        content=artifact.zip_bytes(),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
