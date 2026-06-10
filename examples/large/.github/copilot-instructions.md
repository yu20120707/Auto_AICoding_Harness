# Copilot Instructions

Read `AGENTS.md` before making changes.

Classify each non-trivial task as simple, medium, or complex:

- simple: main agent handles directly with local verification
- medium: use a short plan and consider scanner or reviewer roles
- complex: use large-mode `.ai/*` artifacts and review gates

Do not store project facts here.
Project facts belong in `docs/ai/*`.
Current task state belongs in `.ai/*`.

If a relevant skill is available, use it as guidance, but do not bypass `AGENTS.md`, review gates, or explicit user constraints.
