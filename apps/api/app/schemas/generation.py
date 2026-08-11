from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    template: str = Field(min_length=2, max_length=64)
    description: str = Field(min_length=3, max_length=2000)

class GenerateResponse(BaseModel):
    project_id: str
    status: str
    template: str
    path: str
