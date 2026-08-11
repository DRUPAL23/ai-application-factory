import os
from typing import Any

from openai import OpenAI


class OpenAIProvider:
    name = "openai"

    def __init__(self, model: str | None = None) -> None:
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-5.6")

    def generate(self, system: str, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            instructions=system,
            input=prompt,
        )
        return response.output_text
