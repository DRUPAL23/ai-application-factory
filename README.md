# AI Application Factory

Reusable, AI-assisted application engineering template for turning product ideas into production-ready software.

## What this repository provides

- AI engineering rules and reusable prompts
- Development container for Codespaces/VS Code
- Python/FastAPI API foundation
- Docker and Compose scaffolding
- GitHub Actions CI, container publishing and deployment hooks
- Kubernetes deployment scaffolding
- Issue and pull-request templates
- Architecture, security and deployment documentation
- Pytest-based testing foundation

## Development lifecycle

```text
Idea → PRD → Architecture → Implementation → Tests → PR → CI → Image → Staging → Production → Monitoring
```

## Quick start

```bash
cp .env.example .env
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run the container stack:

```bash
docker compose up --build
```

API health check: `GET /health`

## Repository map

```text
.github/              CI/CD and contribution templates
.devcontainer/        Reproducible development environment
docs/                 Architecture, development, deployment and security
apps/api/             FastAPI application and tests
packages/             Reusable AI/application packages
docker/               Container build assets
kubernetes/           Kubernetes deployment manifests
scripts/              Local automation helpers
```

## AI workflow

Read `AI_ENGINEERING_RULES.md` before implementing changes. For substantial work, first create or update the architecture/requirements documentation, then implement in small, testable increments.

## Creating a new application from this template

1. Use this repository as a GitHub template.
2. Rename the generated project.
3. Replace project-specific requirements and architecture placeholders.
4. Set repository Actions secrets/variables.
5. Configure deployment targets.
6. Enable branch protection and required CI checks.
7. Start feature development from a branch.

See `docs/DEVELOPMENT.md`, `docs/DEPLOYMENT.md`, and `docs/ARCHITECTURE.md`.
