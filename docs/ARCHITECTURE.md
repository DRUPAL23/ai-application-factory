# Architecture

## Purpose

A reusable application factory that provides a production-oriented foundation for AI-assisted application generation and delivery.

## Reference architecture

```text
Client
  ↓
Ingress / Reverse Proxy / WAF
  ↓
API service (FastAPI)
  ├── AI orchestration packages
  ├── domain/application services
  ├── background workers (optional)
  └── external providers
       ↓
PostgreSQL     Redis     Object Storage

Delivery:
GitHub → Pull Request → GitHub Actions → Test/Build/Security → Container Registry → Staging → Production
```

## Boundaries

- `apps/api`: deployable API application.
- `packages`: reusable application/AI modules.
- `docker`: container build assets.
- `kubernetes`: deployment manifests.
- `.github`: repository automation and contribution workflows.
- `docs`: durable engineering and operational knowledge.

## Reliability principles

- Stateless API processes where practical.
- Persistent state belongs in managed/persistent services.
- Health/readiness checks are mandatory for deployable services.
- Configuration comes from environment/secrets, not source code.
- Database migrations must be reviewed for compatibility and data loss risk.
- Production changes must be observable and reversible.

## Security boundaries

External input is untrusted. Authentication and authorization are distinct concerns. Secrets must be injected at runtime. Logs must not contain credentials or sensitive payloads.

## Scaling path

Start with a small deployable service. Add replicas, caching, workers, queues, read replicas or service decomposition only when measured load or reliability requirements justify the complexity.
