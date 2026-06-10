# Scripts

This directory is for target-project helper script templates and repository-level
utility notes.

The user-facing command entrypoints live in `bin/`.
Shared command logic lives in `core/`.
Generated target-project script templates live under `templates/base/root/scripts/`.

Do not move command implementations into this directory unless the repository
contracts are intentionally changed.

## Current Generated Script Templates

- `templates/base/root/scripts/ai_build.sh`
- `templates/base/root/scripts/ai_test.sh`
- `templates/base/root/scripts/ai_check.sh`

Those scripts are placeholders for target projects to adapt. They are not the
harness CLI implementation.
