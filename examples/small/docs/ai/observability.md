# Observability

Use this guide when changing backend or system behavior that needs to be diagnosed after it runs outside the current session.

## Review Focus

- logs that identify the operation, resource, peer, or request involved
- error messages that preserve root-cause context
- metrics for latency, throughput, failures, retries, queue depth, and resource use
- startup, shutdown, retry, and background worker visibility
- distinction between transient and permanent failures
- production-safe diagnostics that do not expose secrets

## C++ / Linux Notes

- Include errno or system error context when it materially helps diagnosis.
- Avoid noisy logs in hot paths unless rate-limited or clearly justified.
- Prefer structured or consistently formatted logs when the project already has a logging convention.
- Make retry loops and timeout paths observable.
- For long-running services, preserve enough state to debug fd leaks, stuck threads, and connection churn.

## Do Not

- Do not log API keys, tokens, passwords, private payloads, or credentials.
- Do not claim operational readiness without logs, metrics, or a clear diagnostic path.
- Do not hide failures by converting them into silent retries.
- Do not add broad logging churn unrelated to the task.
