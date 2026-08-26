# Development Guide

## Branches

Use short-lived branches:

- `feature/<name>`
- `fix/<name>`
- `refactor/<name>`
- `chore/<name>`

Open a pull request into `main` after local checks pass.

## Local API

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker compose up --build
```

## AI-assisted implementation

Before coding, define the requirement and acceptance criteria. Ask the AI agent to inspect the repository and propose affected files. Implement one bounded change at a time, then run tests and review the diff.

## Quality gates

Every pull request should pass:

- syntax/type/static checks appropriate to the stack
- unit/integration tests
- application build
- container build when deployment assets change

## Commit convention

Use conventional prefixes such as `feat:`, `fix:`, `refactor:`, `test:`, `docs:` and `chore:`.

## Pull requests

Describe the problem, implementation, tests, security impact, migrations and deployment implications. Keep changes focused.
