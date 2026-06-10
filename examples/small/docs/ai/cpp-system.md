# C++ System Engineering

## Core Rules

- Use RAII for resource ownership whenever possible.
- State resource lifetime explicitly for every non-trivial change.
- Treat file descriptors, sockets, threads, mutexes, shared memory, and semaphores as owned resources with explicit release paths.
- Document error-code and exception boundaries. Do not mix them casually.
- Preserve copy and move semantics intentionally. Do not change them accidentally.
- Assume public header changes can affect downstream build stability and ABI.
- Prefer the smallest change that solves the problem.

## Resource Management

- Explain who owns each fd, socket, thread, mutex, shm region, or sem handle.
- Explain when the resource is created, handed off, and released.
- Watch object lifetime versus callback, thread, and event-loop lifetime.
- Avoid raw owning pointers when a standard owner type or dedicated wrapper is clearer.

## Interface Risk

- Call out public header impact before changing exported types or signatures.
- Check API and ABI risk for:
  - function signatures
  - class layout
  - vtable-affecting changes
  - inline behavior in headers
  - enum and error-code changes

## Validation

- For every non-trivial C++ system change, explain ownership, lifetime, error handling, and validation.
- If build or tests are not run, say why and what should be run next.
