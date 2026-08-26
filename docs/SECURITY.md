# Security

## Baseline

- Never commit secrets.
- Validate and constrain external input.
- Enforce authentication and authorization separately.
- Apply least privilege to GitHub, cloud and runtime identities.
- Keep databases and Redis on private networks.
- Pin or regularly review dependencies and action versions.
- Scan dependencies and container images in CI.
- Avoid sensitive data in logs.
- Use TLS for external traffic.
- Review file uploads, SSRF, injection, XSS, CSRF and deserialization risks where applicable.

## Incident response

1. Contain the affected system or credential.
2. Rotate compromised secrets.
3. Preserve relevant logs and evidence.
4. Identify scope and root cause.
5. Patch and test.
6. Deploy through the normal CI/CD gates.
7. Document the incident and prevention actions.
