from dataclasses import dataclass

from packages.ai_engine.engine import AIEngine
from packages.generator.generator import ProjectGenerator


@dataclass
class ApplicationOrchestrator:
    ai_engine: AIEngine | None = None
    generator: ProjectGenerator | None = None

    def __post_init__(self) -> None:
        self.ai_engine = self.ai_engine or AIEngine()
        self.generator = self.generator or ProjectGenerator()

    def run(self, prompt: str, project_name: str) -> dict:
        specification = self.ai_engine.plan(prompt, project_name)
        files = self.generator.generate(specification)
        return {
            "project": specification["project"],
            "stack": specification["stack"],
            "files": files,
            "status": "generated",
        }
