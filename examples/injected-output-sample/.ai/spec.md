# Spec

## Outcome

Document a realistic large-mode task for the sample server repository so the
example shows more than raw initialization output.

## Requested Change

- keep the business surface intentionally small: `Server`, its textual
  description, and one minimal test
- show how a large-mode task is scoped around that business code without
  pretending the scaffold already performed the implementation
- keep the example repository self-contained and easy to compare with
  `examples/cpp-linux-backend-mini/`

## Constraints

- do not expand the sample into a real networking stack
- do not introduce runtime noise such as backups, handoff drafts, or context
  packs
- keep the harness-managed task id aligned across `.ai/state.json` and
  `docs/ai/tasks/`

## Non-Goals

- demonstrating a finished human approval chain
- replacing `templates/` as the source of truth
