# Risk And Rollback

## Residual Risks

- readers may mistake the evidence chain for a completed workflow if the task
  docs stay too generic
- future template changes can drift away from this committed snapshot

## Rollback

- if the example becomes misleading, regenerate it from the current templates
  and profile overlay
- if only task naming drifts, realign `.ai/state.json` and
  `docs/ai/tasks/<task-id>/`

## Required Follow-Up

- keep `tests/test_examples.py` synchronized with any future example changes
