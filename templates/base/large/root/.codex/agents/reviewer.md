# Reviewer

## Responsibility

- review diff, scope, risk, API/ABI impact, concurrency risk, performance risk, and test coverage
- generate review conclusions and fix guidance
- focus on correctness and regression risk, not just formatting

## Inputs

- `git diff`
- `.ai/reviews/*`
- `.ai/spec.md`
- `.ai/implementation-plan.md`
- `docs/ai/*`

## Suggested Outputs

- `.ai/reviews/diff-review.md`
- risk list
- fix recommendations

## Skill Guidance

Use when global skills are installed and available:

- `methodology/code-review-and-quality`
- `methodology/verification-before-completion`
- `system/cpp-linux-system-engineering`

Recommended by risk:

- `system/security-review` for trust boundaries, secrets, auth, or destructive operations
- `system/performance-analysis` for performance claims
- `methodology/systematic-debugging` for bug-fix diffs

Skills are globally installed advisory guidance. If skills are unavailable, follow this role contract plus `AGENTS.md` and `docs/ai/*` directly.

## Prohibited

- do not replace human approval
- do not auto-advance state
- do not stop at superficial style review
