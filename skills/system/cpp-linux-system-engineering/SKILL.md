---
name: cpp-linux-system-engineering
description: Use for C++/Linux/backend/system changes involving ownership, lifetime, build, Linux debugging, network IO, concurrency, API/ABI, persistence, or observability.
source: self-authored
upstream: Auto_AICoding_Harness cpp-linux-backend-system profile
license: project-local
adaptation_notes: Expanded into a fuller system-engineering workflow that consolidates prior narrow C++/Linux checks into one reusable skill; defers project facts to `docs/ai/*`.
---

# Cpp Linux System Engineering

## Purpose

Keep C++ / Linux / backend / system work correct across:

- ownership and lifetime
- build behavior
- runtime diagnostics
- network IO
- concurrency
- API/ABI compatibility
- persistence and observability

## Use When

Use when touching:

- C++ source or headers
- CMake or build files
- Linux process behavior
- sockets, epoll, or fd handling
- threads, locks, atomics, or queues
- serialization or protocol code
- config, persistence, logging, metrics, or service lifecycle logic

## Inputs

- `docs/ai/cpp-system.md`
- `docs/ai/linux-debug.md`
- `docs/ai/network.md`
- `docs/ai/concurrency.md`
- `docs/ai/api-abi.md`
- `docs/ai/cmake.md`
- `docs/ai/build.md`
- `docs/ai/testing.md`
- `docs/ai/observability.md`
- current diff
- build/test output

## Process

### 1. Check Ownership and Lifetime First

Review:

- RAII usage
- raw pointer ownership
- move/copy behavior
- reference lifetime
- cleanup on early returns and exceptions

If ownership is unclear, the code is not ready.

### 2. Verify Error-Path Semantics

Check:

- return-code handling
- exception boundaries
- partial failure cleanup
- timeout and retry behavior
- logging of actionable failures

### 3. Review Build Integration

For CMake and build changes:

- target visibility
- include paths
- link dependencies
- compile definitions
- generated-file handling
- machine-local path leakage

Watch for accidental dependency direction changes.

### 4. Use Linux Evidence, Not Guesswork

When runtime behavior is unclear, prefer evidence from:

- `strace`
- `gdb`
- core dumps
- `/proc`
- `lsof`
- `ss`
- `dmesg`
- `journalctl`

Use `strace` when you need syscall truth.
Use `gdb` or core dumps when process state matters.

### 5. Review Network IO Carefully

For socket code, check:

- blocking vs non-blocking mode
- partial read/write handling
- `EINTR`
- `EAGAIN`
- timeout semantics
- framing and message boundaries
- reconnect or backoff behavior

In event-driven paths, review `epoll` registration and wakeup handling carefully.

### 6. Review Concurrency Like a Contract

Check:

- thread ownership and join/detach lifecycle
- lock order
- condition-variable usage
- atomic memory semantics
- shared-state races
- deadlock risk
- shutdown coordination

If multiple threads touch shared state, ask what invariant protects it.

### 7. Check API/ABI and Compatibility

For shared or externally consumed code, review:

- public header changes
- object layout assumptions
- virtual interface changes
- serialization schema changes
- config compatibility
- stored data compatibility

This is where API/ABI notes must be explicit.

### 8. Preserve Operational Observability

Check that the change still gives operators enough signal:

- logs at the right severity
- metrics around failures and retries
- error context without secret leakage
- diagnostics for production incidents

## Output

Produce a bounded implementation or review note with:

- affected files
- system risks
- compatibility impact
- validation commands
- remaining unknowns

## Do Not

- do not leak resources
- do not change public API/ABI/protocol/config without compatibility notes
- do not change timeout, retry, persistence, or concurrency semantics casually
- do not use machine-local build paths
- do not log secrets
