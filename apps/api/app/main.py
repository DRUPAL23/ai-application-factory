from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Application Factory API", version="0.1.0")
app.include_router(router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ai-application-factory-api"}
