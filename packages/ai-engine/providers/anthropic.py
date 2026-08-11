import os

from anthropic import Anthropic


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model: str | None = None) -> None:
        self.client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model or os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")

    def generate(self, system: str, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in response.content if hasattr(block, "text"))
