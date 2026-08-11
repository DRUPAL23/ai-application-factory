from dataclasses import dataclass
from typing import Any, Protocol


class Agent(Protocol):
    name: str

    def run(self, context: dict[str, Any]) -> dict[str, Any]: ...


@dataclass
class RequirementsAgent:
    name: str = "requirements"

    def run(self, context: dict[str, Any]) -> dict[str, Any]:
        return {"requirements": context.get("requirements", [])}
