import os
from typing import Any


class AIEngine:
    """Planning boundary for model providers.

    Uses deterministic planning when no provider is configured, allowing the
    factory pipeline to run locally before an AI provider is connected.
    """

    def plan(self, prompt: str, project_name: str) -> dict[str, Any]:
        provider = os.getenv("AI_PROVIDER", "local")
        return {
            "project": project_name,
            "prompt": prompt,
            "provider": provider,
            "stack": {
                "frontend": "nextjs",
                "backend": "fastapi",
                "database": "postgresql",
                "cache": "redis",
            },
            "requirements": [prompt],
        }
