import re
from typing import Any

from app.blueprints.schemas import ComponentSpec, ProjectBlueprint, RequirementSpec, StackSpec
from app.blueprints.validator import validate_blueprint

FEATURE_RULES: list[tuple[tuple[str, ...], str, str]] = [
    (("login", "authentication", "sign in", "register", "registration"), "Authentication", "Users can securely register and sign in according to defined access rules."),
    (("payment", "mpesa", "m-pesa", "checkout", "billing"), "Payments and checkout", "The application exposes a validated payment or checkout flow and records transaction outcomes."),
    (("admin", "dashboard", "analytics", "reporting"), "Administration and reporting", "Authorized operators can inspect and manage relevant application data."),
    (("product", "catalogue", "catalog", "inventory", "store", "ecommerce", "e-commerce"), "Product and inventory management", "Users can browse or manage products and inventory according to their role."),
    (("social media", "publish", "content", "posts", "marketing"), "Content management", "Users can create, review, and manage publishable content."),
    (("search", "filter", "discover"), "Search and discovery", "Users can find relevant records using a clear search or filtering interface."),
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:100].strip("-") or "generated-project"


class BlueprintCompiler:
    """Compiles an idea into a predictable, reviewable blueprint v1."""

    def compile(
        self,
        prompt: str,
        project_name: str,
        target_platforms: list[str] | None = None,
        preferred_stack: dict[str, str] | None = None,
    ) -> tuple[ProjectBlueprint, dict[str, Any]]:
        prompt = prompt.strip()
        if len(prompt) < 3:
            raise ValueError("Prompt must contain at least 3 characters")
        if not project_name.strip():
            raise ValueError("Project name is required")

        normalized = prompt.lower()
        project_type = self._classify(normalized)
        requirements: list[RequirementSpec] = [
            RequirementSpec(
                id="REQ-001",
                title="Core project behavior",
                description=f"Deliver the core functionality described by the project owner: {prompt[:850]}",
                priority="must",
                acceptance_criteria=["The delivered application implements the approved project scope.", "Unimplemented or simulated behavior is clearly documented."],
            )
        ]
        for _, title, description in FEATURE_RULES:
            keywords = next(rule[0] for rule in FEATURE_RULES if rule[1] == title)
            if any(keyword in normalized for keyword in keywords):
                req_id = f"REQ-{len(requirements) + 1:03d}"
                requirements.append(RequirementSpec(id=req_id, title=title, description=description, priority="must", acceptance_criteria=[f"The {title.lower()} workflow is documented and has a testable expected outcome."]))

        stack_values = {"frontend": "react-vite", "backend": "fastapi", "database": "postgresql", "deployment": "docker"}
        for key, value in (preferred_stack or {}).items():
            if key in stack_values and isinstance(value, str) and value.strip():
                stack_values[key] = value.strip().lower()

        components = [
            ComponentSpec(name="Web Frontend", kind="frontend", responsibilities=["Responsive user interface", "Client-side validation"]),
            ComponentSpec(name="API Backend", kind="backend", responsibilities=["Business rules", "Input validation", "API contracts"], depends_on=["Database"]),
            ComponentSpec(name="Database", kind="database", responsibilities=["Persistent application data"]),
            ComponentSpec(name="Build and Deployment", kind="infrastructure", responsibilities=["Reproducible builds", "Environment configuration"]),
        ]
        if any(term in normalized for term in ("mpesa", "m-pesa", "payment", "third-party", "integration", "webhook")):
            components.append(ComponentSpec(name="External Integrations", kind="integration", responsibilities=["Provider adapters", "Timeouts and retries", "Secret-backed configuration"], depends_on=["API Backend"]))

        blueprint = ProjectBlueprint(
            project_name=project_name.strip(), slug=slugify(project_name), project_type=project_type,
            prompt=prompt, target_platforms=target_platforms or ["web"], stack=StackSpec(**stack_values),
            requirements=requirements, components=components,
            security_requirements=["Validate all untrusted input on the server.", "Keep credentials out of source control and generated artifacts.", "Enforce authentication and authorization for protected operations.", "Run generated code only in an isolated, resource-limited environment."],
            assumptions=["The blueprint is a draft and requires owner review before code generation.", "External services require valid credentials and separate integration testing.", "The selected stack is a default unless explicitly changed by the project owner."],
        )
        return blueprint, validate_blueprint(blueprint)

    @staticmethod
    def _classify(prompt: str) -> str:
        if any(word in prompt for word in ("ecommerce", "e-commerce", "online store", "shopping cart", "product catalogue", "mpesa checkout")):
            return "ecommerce"
        if any(word in prompt for word in ("saas", "subscription", "multi-tenant")):
            return "saas"
        if any(word in prompt for word in ("rest api", "api service", "backend api")):
            return "api"
        if any(word in prompt for word in ("dashboard", "analytics dashboard", "admin panel")):
            return "dashboard"
        if any(word in prompt for word in ("mobile app", "android app", "ios app")):
            return "mobile_app"
        if any(word in prompt for word in ("automation", "workflow automation", "scheduled job")):
            return "automation"
        if any(word in prompt for word in ("ai app", "ai assistant", "llm", "language model")):
            return "ai_app"
        if any(word in prompt for word in ("website", "landing page", "web page")):
            return "website"
        return "other"
