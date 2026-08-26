# AI Engineering Rules

## Operating principles

1. Treat the repository as the source of truth.
2. Inspect existing architecture before changing code.
3. Make the smallest safe change that satisfies the requirement.
4. Do not modify unrelated files.
5. Do not introduce dependencies without justification.
6. Never commit secrets, credentials, tokens, private keys or production data.
7. Validate all untrusted input at system boundaries.
8. Keep business logic out of transport/controller layers.
9. Add or update tests for behavior changes.
10. Preserve backward compatibility unless a breaking change is explicitly approved.
11. Document migrations, breaking changes and architectural decisions.
12. Do not claim tests, builds or deployments succeeded unless they actually ran.
13. Prefer deterministic, observable and reversible changes.
14. Review generated code for security, correctness and maintainability.
15. Keep AI-generated changes reviewable; avoid giant unrelated patches.

## Definition of done

- Requirements and acceptance criteria are satisfied.
- Tests cover new or changed behavior.
- Lint/type/static checks pass where configured.
- Build/package succeeds.
- Security implications have been reviewed.
- Documentation is updated when behavior or operations change.
- CI passes.
- Deployment/rollback implications are understood.

## AI task protocol

For non-trivial work:

1. Summarize the current state.
2. Identify affected files.
3. Propose the implementation.
4. Implement incrementally.
5. Run relevant checks.
6. Review the diff for regressions and security issues.
7. Report changed files, checks run, failures and remaining risks.
