# Cpp System Dev

## Purpose

Keep C++ system changes safe around RAII, ownership, lifetime, and minimal diff expectations.

## Use When

Editing C++ backend or system code that touches fd, socket, thread, mutex, shm, sem, error handling, or copy / move behavior.

## Inputs

`AGENTS.md`, `docs/ai/cpp-system.md`, `docs/ai/api-abi.md`, the current diff, and relevant build or test output.

## Process

Review ownership and lifetime, check resource handling for fd / socket / thread / mutex / shm / sem, inspect error paths, confirm copy / move behavior, and keep the diff minimal.

## Output

A bounded implementation or review note that preserves ownership, lifetime, and error-handling correctness.

## Do Not

Do not leak resources.
Do not change public headers without API/ABI review.
Do not ignore error paths.
