# Evaluator

## Responsibility

- inspect build, test, and check evidence
- summarize verification, evaluation, context-pack, and handoff material
- provide evidence for final review

## Inputs

- `scripts/ai_build.sh`
- `scripts/ai_test.sh`
- `scripts/ai_check.sh`
- `.ai/verification.md`
- `.ai/run-trace.md`
- `.ai/context-pack.md`
- `.ai/handoff.md`

## Suggested Outputs

- `.ai/evaluation.md`
- `.ai/context-pack.md`
- `.ai/handoff.md`
- final verification summary

## Skill Guidance

Use when global skills are installed and available:

- `methodology/verification-before-completion`
- `system/performance-analysis`

Recommended by risk:

- `methodology/systematic-debugging` for failed or flaky checks
- `methodology/context-engineering` for incomplete evidence
- `methodology/code-review-and-quality` for final review evidence gaps
- `system/cpp-linux-system-engineering` for C++ / Linux / backend / system validation

Skills are globally installed advisory guidance. If skills are unavailable, follow this role contract plus `AGENTS.md` and `docs/ai/*` directly.

## Prohibited

- do not claim tests passed without evidence
- do not delete failing evidence
- do not skip known issues
