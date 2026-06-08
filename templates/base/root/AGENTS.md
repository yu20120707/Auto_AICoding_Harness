# AGENTS.md

## Project Type

This repository uses `Auto_AICoding_harness` base workflow.

## Required Reading

Read `docs/ai/README.md` first.

For non-trivial tasks, also read the relevant `docs/ai/*` files for the area you are changing.

Always read active `.ai/` task files when they exist.

For C++ / Linux / backend / system work, pay attention to:

- ownership and lifetime
- concurrency and lock scope
- API / ABI compatibility
- performance evidence
- build and test validation

## Workflow

- `small` and `large` share one workflow model
- `small` requires `diff` and `final`
- `large` requires `spec`, `plan`, `diff`, and `final`

## Safety

- do not overwrite existing files unless explicitly allowed
- do not treat `.ai/` as long-lived architecture knowledge
- do not bypass review gates or safe-write rules
- do not refactor unrelated code opportunistically
