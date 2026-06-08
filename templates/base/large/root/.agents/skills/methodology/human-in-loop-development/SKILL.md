# Human In Loop Development

## Purpose

Enforce human gates for spec / plan / diff / final.

## Use When

Any workflow with `WAITING_HUMAN_*` status.

## Inputs

`.ai/state.json`, `.ai/reviews/*`, and `.ai/approvals/*`.

## Process

Stop at waiting gates, request human approve or reject input, and continue only through the explicit commands.

## Output

A workflow that respects the active waiting gate and review artifacts.

## Do Not

Do not auto-approve.
Do not continue after `WAITING_HUMAN_*`.
Do not change state manually outside commands.
