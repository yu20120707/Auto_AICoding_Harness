# docs/ai

This directory stores long-lived project knowledge for a generated target repository.

Read this directory before making non-trivial changes.

Typical contents:

- architecture notes
- build and test entrypoints
- review checklists
- workflow rules that should survive individual tasks
- risk notes that outlive a single task

For `cpp-linux-backend-system` projects, start with:

- `docs/ai/workflow.md`
- `docs/ai/cpp-system.md`
- `docs/ai/linux-debug.md`
- `docs/ai/network.md`
- `docs/ai/concurrency.md`
- `docs/ai/api-abi.md`
- `docs/ai/performance.md`
- `docs/ai/cmake.md`
- `docs/ai/build.md`
- `docs/ai/testing.md`

Task runtime state does not belong here.
Task runtime belongs in `.ai/`.
