# Blueprint Engine v1

## Purpose

The Blueprint Engine converts a project idea into a typed, versioned draft specification before code generation. It is deterministic in v1: it does not claim that an AI model interpreted or validated the idea, and it does not execute generated code.

## Draft workflow

1. Normalize the project name and prompt.
2. Classify the project using transparent keyword rules.
3. Create stable requirement IDs and acceptance criteria.
4. Select a default stack, applying only recognized caller overrides.
5. Describe application components and dependencies.
6. Add baseline security requirements and assumptions.
7. Run deterministic schema and dependency validation.
8. Return the blueprint plus findings for owner review.

## Contract

`ProjectBlueprint` is the canonical Pydantic v2 model. `schema_version` starts at `1.0`. Consumers should not rely on unversioned internal fields. Requirements use `REQ-NNN` IDs and must include acceptance criteria. Component dependencies refer to component names.

## API

`POST /api/v1/blueprints` accepts:

```json
{
  "project_name": "Kenya Commerce",
  "prompt": "Build an ecommerce website with M-Pesa checkout and an admin dashboard",
  "target_platforms": ["web"],
  "preferred_stack": {"frontend": "react-vite", "backend": "fastapi"}
}
```

The response includes `blueprint`, `validation`, and `status: draft`. A successful schema validation does not mean source code has been generated, tested, secured, or deployed. `execution_status` remains `not_run` at this stage.

## Known limitations

- Classification and feature extraction are keyword-based; they can miss intent and produce false positives.
- A human must review the draft before code generation.
- Stack overrides are not yet checked against a supported template registry.
- This release does not persist blueprints or invoke external AI providers.

## Next milestones

- Connect the AI provider abstraction to requirements extraction with schema-constrained output.
- Add blueprint persistence and revision history.
- Map approved components to generator templates.
- Add build sandbox, test evidence, and artifact export.
