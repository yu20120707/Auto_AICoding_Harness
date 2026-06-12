# Verification

Record concrete validation evidence here.

## Ran

- command: not run in the committed example snapshot
- result: n/a
- notes: this example is meant to show the scaffold shape, not to claim a
  completed engineering task

## Not Run

- item: compile and run `tests/test_server.cpp`
- reason: committed examples are static snapshots, not CI artifacts
- required follow-up: use the generated `scripts/ai_build.sh`,
  `scripts/ai_test.sh`, or the target project's own build/test flow
- item: large-mode human review gates
- reason: this sample is frozen at task setup time
- required follow-up: run `ai-review spec`, `ai-review plan`, `ai-review diff`,
  and `ai-review final` in a real target repository
