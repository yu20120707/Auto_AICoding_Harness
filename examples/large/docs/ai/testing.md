# Testing Guidance

## Test Types

- unit tests
- integration tests
- regression tests
- manual validation when automation is not available

## C++ Defaults

- use CTest where the project already exposes it
- use GTest where it is the project standard
- keep failing tests visible

## Rules

- Do not delete failing tests to make the suite pass.
- If tests were not run, state why.
- If a manual check was used, record the exact command or procedure.
- Regression-sensitive fixes should mention how recurrence is prevented.
