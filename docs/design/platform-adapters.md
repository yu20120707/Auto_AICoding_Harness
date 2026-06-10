# Platform Adapters

## Decision

This repository is `Codex-first, multi-agent-compatible`.
It provides portable sources and lightweight setup guidance instead of owning a heavy adapter for every AI coding surface.

## Why

AI coding tools differ in where they load instructions and skills.
A hard-coded installer for every surface would be brittle and expensive to maintain.
The safer model is to provide clear sources, suggested targets, and a bootstrap prompt that lets the active local agent install the right subset.

## Supported Surfaces

### Codex

- Canonical skill source: `skills/`
- Example installer: `bin/ai-install-skills`
- Dry-run inspection: `bin/ai-install-skills --dry-run`
- Target-project entrypoint: `AGENTS.md`
- Runtime state: `.ai/*`

### Claude Code

- Suggested global instruction target: `~/.claude/CLAUDE.md`
- Suggested skill target: `~/.claude/skills/<skill-name>/`
- Suggested project entrypoints: `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`
- This repository does not yet generate Claude-specific project files by default.

### GitHub Copilot / VS Code

- Suggested always-on project instruction: `.github/copilot-instructions.md`
- Suggested path-specific instructions: `.github/instructions/*.instructions.md`
- Suggested skill targets: `.github/skills/<skill-name>/`, `~/.copilot/skills/<skill-name>/`, or `~/.agents/skills/<skill-name>/`
- This repository generates a lightweight Copilot trigger instruction, not a full duplicated skill tree.

### Generic Agents

Generic agents should read:

1. `AGENTS.md`
2. `docs/ai/README.md`
3. relevant `docs/ai/*`
4. `skills/README.md` when skill installation is requested
5. `docs/install-targets.md` when global setup is requested

## Non-Goals

- no implicit global writes during clone
- no automatic third-party skill fetching
- no mandatory platform plugin framework
- no single fixed global `AGENTS.md` location
- no duplicated project facts in global instructions

## Current Automation Boundary

Only Codex has an implemented example installer.
Claude Code, GitHub Copilot / VS Code, and generic agents are supported through documented install targets and the bootstrap prompt.
They are not configured by `ai-install-skills`.
