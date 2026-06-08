---
name: cpp-linux-system-engineering
description: Use for C++/Linux/backend/system changes involving ownership, lifetime, build, Linux debugging, network IO, concurrency, API/ABI, persistence, or observability.
source: self-authored
upstream: Auto_AICoding_Harness cpp-linux-backend-system profile
license: project-local
adaptation_notes: Consolidates prior narrow C++/Linux system skills into one system-level skill that points to docs/ai/* for detail.
---

# Cpp Linux System Engineering

## Purpose

Keep C++ / Linux / backend / system work correct across resource ownership, build behavior, runtime diagnostics, concurrency, compatibility, and operations.

## Use When

Use when touching C++ source, CMake/build files, Linux process behavior, sockets, epoll, fd handling, threads, locks, atomics, public headers, serialization, config, persistence, logging, metrics, or service lifecycle code.

## Inputs

`docs/ai/cpp-system.md`, `docs/ai/linux-debug.md`, `docs/ai/network.md`, `docs/ai/concurrency.md`, `docs/ai/api-abi.md`, `docs/ai/cmake.md`, `docs/ai/build.md`, `docs/ai/testing.md`, `docs/ai/observability.md`, current diff, and build/test output.

## Process

Check RAII, ownership, lifetime, and error paths.
Check CMake target scope, link dependencies, generated build directories, and compile commands.
Check Linux evidence with logs, `/proc`, `strace`, `gdb`, core dumps, `lsof`, `ss`, `dmesg`, or `journalctl` when relevant.
Check socket lifecycle, partial read/write, `EINTR` / `EAGAIN`, non-blocking IO, `epoll`, timeout, retry, and framing behavior.
Check thread lifetime, lock order, `condition_variable`, atomics, shared state, data races, deadlocks, and object lifetime.
Check public headers, API/ABI, protocol, serialization, config, stored data, and version compatibility.
Check observability for logs, metrics, retry visibility, and production-safe diagnostics.

## Output

A bounded implementation or review note with affected files, system risks, compatibility impact, validation commands, and remaining unknowns.

## Do Not

Do not leak resources.
Do not change public API/ABI/protocol/config without compatibility notes.
Do not change timeout, retry, persistence, or concurrency semantics casually.
Do not use machine-local build paths.
Do not log secrets.
