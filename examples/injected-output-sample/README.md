# injected-output-sample

This directory shows a target-project snapshot after harness injection and one
large-mode task setup.

It is meant to answer:

- what a business repository looks like after `ai-init small`
- what gets added when the same repository upgrades into `large`
- how `docs/ai/tasks/<task-id>/` mirrors the large-mode evidence chain
- where business code ends and harness-managed files begin

The business source tree here is intentionally tiny.
The active sample task is `sample-server-hardening`, which uses the tiny server
under `include/`, `src/`, and `tests/` as the business surface and the
`docs/ai/tasks/sample-server-hardening/` directory as the mirrored large-mode
evidence chain.

These harness artifacts are illustrative and should be compared with
`templates/` and `profiles/`, which remain the source of truth.
