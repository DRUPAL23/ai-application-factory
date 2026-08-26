# Testing Guide

The API uses pytest as the baseline test framework.

## Test layers

- Unit: isolated business logic.
- Integration: service/database/API boundaries.
- End-to-end: critical user journeys.
- Smoke: deployment health and critical endpoints.

## Commands

```bash
cd apps/api
pytest -q
python -m compileall app
```

## Test requirements

New behavior should include tests for the happy path, validation failures, authorization failures, boundary values and relevant provider failures.

## CI policy

A pull request is not ready when tests are skipped to make the pipeline green. Fix the underlying failure or explicitly document the exception.
