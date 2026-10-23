from collections import Counter
from typing import Any

from app.blueprints.schemas import ProjectBlueprint


def validate_blueprint(blueprint: ProjectBlueprint) -> dict[str, Any]:
    """Return deterministic quality findings; never marks code as built or tested."""
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    requirement_ids = [item.id for item in blueprint.requirements]
    duplicates = [key for key, count in Counter(requirement_ids).items() if count > 1]
    for duplicate in duplicates:
        errors.append({"code": "duplicate_requirement_id", "message": f"Duplicate requirement ID: {duplicate}"})

    component_names = {item.name for item in blueprint.components}
    for component in blueprint.components:
        for dependency in component.depends_on:
            if dependency not in component_names:
                errors.append({"code": "unknown_component_dependency", "message": f"Component '{component.name}' depends on unknown component '{dependency}'"})

    for requirement in blueprint.requirements:
        if not requirement.acceptance_criteria:
            errors.append({"code": "missing_acceptance_criteria", "message": f"Requirement {requirement.id} has no acceptance criteria"})
    if not blueprint.security_requirements:
        warnings.append({"code": "security_requirements_missing", "message": "Add explicit security requirements before production release."})
    if blueprint.stack.database.lower() in {"none", "n/a", "na"} and blueprint.project_type in {"ecommerce", "saas"}:
        warnings.append({"code": "data_persistence_review", "message": "This project type commonly needs durable data storage; confirm the database decision."})

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "requirements_have_acceptance_criteria": all(bool(r.acceptance_criteria) for r in blueprint.requirements),
            "requirement_ids_unique": not duplicates,
            "component_dependencies_resolve": not any(e["code"] == "unknown_component_dependency" for e in errors),
        },
        "execution_status": "not_run",
    }
