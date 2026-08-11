import json
import os
from typing import Any

from packages.ai_engine.providers.anthropic import AnthropicProvider
from packages.ai_engine.providers.local import LocalProvider
from packages.ai_engine.providers.openai import OpenAIProvider
from packages.ai_engine.prompts.generation import ARCHITECTURE_PROMPT, SYSTEM_PROMPT


class AIEngine:
    def __init__(self, provider: Any | None = None) -> None:
        if provider is not None:
            self.provider = provider
        else:
            name = os.getenv("AI_PROVIDER", "local").lower()
            if name == "openai":
                self.provider = OpenAIProvider()
            elif name == "anthropic":
                self.provider = AnthropicProvider()
            else:
                self.provider = LocalProvider()
        self.provider_name = self.provider.name

    def plan(self, prompt: str, project_name: str) -> dict[str, Any]:
        if self.provider_name == "local":
            return {
                "project": project_name,
                "prompt": prompt,
                "provider": self.provider_name,
                "stack": {
                    "frontend": "nextjs",
                    "backend": "fastapi",
                    "database": "postgresql",
                    "cache": "redis",
                },
                "requirements": [prompt],
            }

        raw = self.provider.generate(
            SYSTEM_PROMPT,
            f"Project: {project_name}\nUser request: {prompt}\n\n{ARCHITECTURE_PROMPT}\nReturn valid JSON with keys: project, requirements, stack, architecture.",
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("AI provider returned invalid architecture JSON") from exc
