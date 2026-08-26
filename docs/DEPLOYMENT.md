# Deployment Guide

## Environments

```text
development → staging → production
```

## Required configuration

Copy `.env.example` to `.env` for local work. In CI/CD, store credentials in GitHub Actions secrets or the target platform's secret manager.

## Container delivery

1. Run CI checks.
2. Build the application image.
3. Tag the image with an immutable version/SHA.
4. Push it to a trusted container registry.
5. Deploy to staging.
6. Run smoke/health checks.
7. Promote the same image to production.

## Kubernetes

The `kubernetes/` directory contains the deployment baseline. Review resource limits, probes, secrets, storage, ingress/TLS and network policies before production use.

Example:

```bash
kubectl apply -k kubernetes/
kubectl rollout status deployment/api -n ai-application-factory
```

## VPS/Docker

Use a reverse proxy with TLS, persistent volumes for stateful services, firewall rules, automatic security updates and a backup strategy. Do not expose PostgreSQL or Redis directly to the public internet.

## Rollback

Keep previous image versions available. Roll back the workload to the last known-good immutable image, verify health, then investigate the failed release before retrying.

## Database changes

Use reviewed, forward-compatible migrations. Back up production data before risky migrations and define an explicit rollback or recovery procedure.

## Production checklist

- [ ] Secrets configured
- [ ] TLS configured
- [ ] Database backup verified
- [ ] Health/readiness checks verified
- [ ] Monitoring and alerts enabled
- [ ] CI passed
- [ ] Staging smoke tests passed
- [ ] Rollback procedure tested
