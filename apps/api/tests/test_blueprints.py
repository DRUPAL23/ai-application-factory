from app.blueprints.compiler import BlueprintCompiler, slugify
from app.blueprints.schemas import ProjectBlueprint
from app.blueprints.validator import validate_blueprint


def test_compiler_creates_reviewable_blueprint():
    blueprint, report = BlueprintCompiler().compile(
        "Build an ecommerce website with M-Pesa checkout, product catalogue, login and admin dashboard",
        "Kenya Commerce",
    )
    assert isinstance(blueprint, ProjectBlueprint)
    assert blueprint.project_type == "ecommerce"
    assert blueprint.slug == "kenya-commerce"
    assert {r.title for r in blueprint.requirements} >= {"Core project behavior", "Payments and checkout", "Authentication"}
    assert report["valid"] is True
    assert report["execution_status"] == "not_run"


def test_slugify_handles_symbols_and_empty_names():
    assert slugify("My Super App!!") == "my-super-app"
    assert slugify("!!!") == "generated-project"


def test_validator_flags_unknown_dependencies():
    blueprint, _ = BlueprintCompiler().compile("Build a website", "Demo")
    data = blueprint.model_dump()
    data["components"][0]["depends_on"] = ["Missing Component"]
    invalid = ProjectBlueprint.model_validate(data)
    report = validate_blueprint(invalid)
    assert report["valid"] is False
    assert report["errors"][0]["code"] == "unknown_component_dependency"


def test_compiler_rejects_short_prompts():
    try:
        BlueprintCompiler().compile("hi", "Demo")
    except ValueError as exc:
        assert "3 characters" in str(exc)
    else:
        raise AssertionError("Expected short prompt to be rejected")
