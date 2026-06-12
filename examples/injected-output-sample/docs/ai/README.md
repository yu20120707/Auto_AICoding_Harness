# docs/ai

This project uses the `cpp-linux-backend-system` profile.

Read the relevant documents here before changing non-trivial C++ / Linux / backend / system code.

Recommended reading by task type:

- C++ ownership, lifetime, and public headers: `cpp-system.md`
- Linux process and kernel debugging: `linux-debug.md`
- sockets, IO, retry, timeout, epoll: `network.md`
- threads, atomics, lock order, shared state: `concurrency.md`
- API, ABI, protocol, config compatibility: `api-abi.md`
- performance and profiling changes: `performance.md`
- logging, metrics, diagnostics, and operational readiness: `observability.md`
- CMake and build graph changes: `cmake.md`
- project build entrypoints and compile database notes: `build.md`
- unit, integration, and regression expectations: `testing.md`

If a change crosses several areas, read all relevant files first and keep the task notes explicit about ownership, compatibility, validation, and rollback.
