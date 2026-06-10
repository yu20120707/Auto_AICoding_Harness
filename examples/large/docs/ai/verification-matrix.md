# C++ Linux Backend System Verification Matrix

This file maps common risk triggers to target-project verification actions.
It is profile guidance, not a core state-machine rule.

## Default Entry Points

Use the target repository scripts first:

- `scripts/ai_build.sh`
- `scripts/ai_test.sh`
- `scripts/ai_check.sh`

Each target project should adapt those scripts to its real build system.
The harness must not assume CMake, CTest, clang-tidy, sanitizers, or benchmark
tools are available unless the target project opts in.

## Risk Matrix

| Risk Trigger | Minimum Verification | Stronger Verification |
| --- | --- | --- |
| Build files, compile flags, or toolchain behavior changed | Run `scripts/ai_build.sh` | Also inspect generated compile commands and run a clean build |
| Public headers, exported symbols, or API contracts changed | Run build and targeted tests | Add ABI/API compatibility review and downstream compile checks |
| Ownership, lifetime, or RAII behavior changed | Run targeted unit tests | Add sanitizer run if the target project supports it |
| Threading, locking, atomics, or async lifecycle changed | Run targeted concurrency tests | Add stress/repetition tests and review lock ordering |
| Network IO, retry, timeout, or backpressure changed | Run targeted integration tests | Add failure injection for timeout, EAGAIN, disconnect, and partial reads/writes |
| Persistence, recovery, or state transition changed | Run state-focused regression tests | Add crash/restart or rollback validation when available |
| Performance-sensitive path changed | Record a baseline and compare | Add P50/P95/P99, throughput, CPU, memory, and allocation measurements |
| Observability, logging, metrics, or tracing changed | Run `scripts/ai_check.sh` | Verify dashboards, metric names, log volume, and alert semantics |
| Security-sensitive parsing, filesystem, subprocess, or network boundary changed | Run tests and inspect inputs | Add focused security review before approval |

## Completion Standard

Before claiming completion, record:

- which script or command was run
- what passed
- what was not run and why
- whether the remaining risk needs human review

Do not claim sanitizer, benchmark, integration, or production-equivalent coverage
unless that evidence was actually produced.
