# Install Targets

This repository provides sources, not a mandatory installer for every AI coding tool.
The preferred setup path is: ask the active local agent to inspect this file and install only the files its own environment supports.

`bin/ai-install-skills` is the Codex example installer. It does not configure Claude Code, GitHub Copilot, VS Code, or generic agents.

## Source Files

- `global/AGENTS.md.template`: user-level behavior baseline.
- `skills/**/SKILL.md`: repository-owned skills.
- `prompts/bootstrap-local-agent.md`: setup prompt for the active local agent.
- `templates/base/root/AGENTS.md`: thin target-project entrypoint.
- `templates/base/root/.github/copilot-instructions.md`: target-project Copilot trigger instructions.

## Recommended Targets

| Surface | Global Instructions | Skills | Project Instructions |
| --- | --- | --- | --- |
| Codex | user-managed global instructions if supported by the local Codex surface | `~/.codex/skills/<skill-name>/` or `$CODEX_HOME/skills/<skill-name>/` | `AGENTS.md` |
| Claude Code | `~/.claude/CLAUDE.md` or another user-level Claude memory file | `~/.claude/skills/<skill-name>/` | `AGENTS.md`, `CLAUDE.md`, or `.claude/CLAUDE.md` |
| GitHub Copilot / VS Code | user profile instructions or `.github/copilot-instructions.md` in a workspace | `~/.copilot/skills/<skill-name>/`, `~/.agents/skills/<skill-name>/`, or project `.github/skills/<skill-name>/` | `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `AGENTS.md` |
| Generic agent | the nearest supported global instruction file | any supported `SKILL.md` discovery root | `AGENTS.md` |

## Current Support Level

| Surface | Current Automation |
| --- | --- |
| Codex | `bin/ai-install-skills` installs a manifest-selected subset into `$CODEX_HOME/skills` or `~/.codex/skills`. Use `--dry-run`, `--list`, `--scope system`, or `--profile cpp-linux-backend-system` to inspect or refine the selection. |
| Claude Code | Documentation and bootstrap prompt only. The active local agent should choose the supported target path. |
| GitHub Copilot / VS Code | Documentation and generated `.github/copilot-instructions.md` only. No automatic skill install is performed. |
| Generic agent | Documentation and bootstrap prompt only. |

## Operating Rules

- Do not install anything implicitly during `git clone`.
- Do not overwrite existing global files without a backup or explicit user approval.
- Use `bin/ai-install-skills --dry-run` before writing Codex skills when the target directory is unclear.
- Use `bin/ai-install-skills --list` to inspect the current manifest selection before writing files.
- Prefer symlinks when the local tool supports them and the repository path is stable.
- Prefer copies when the target tool does not support symlinks well.
- Keep global instructions short; put repository facts in each target project's `docs/ai/*`.
- Keep skills portable; avoid tool-specific commands in `SKILL.md` unless the skill is explicitly platform-specific.
- Treat `skill.yaml` as the selection contract for default installs, scope filters, profile filters, and the installed-skills manifest.

## Evidence Behind The Targets

- `AGENTS.md` is a predictable project-level instruction file for coding agents.
- GitHub Copilot supports repository instructions, path-specific instructions, agent instructions, and agent skills.
- VS Code supports always-on `.github/copilot-instructions.md`, `AGENTS.md`, and `CLAUDE.md`, plus file-based `.instructions.md`.
- Claude Code supports project/user memory via `CLAUDE.md` and modular rules under `.claude/rules/`.
