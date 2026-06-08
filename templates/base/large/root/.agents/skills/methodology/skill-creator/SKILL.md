---
name: skill-creator
description: Use when creating or updating local project-level skills, including SKILL.md structure, concise trigger metadata, provenance, and validation checks.
source: adapted
upstream: openai/codex skill-creator
license: see-upstream
adaptation_notes: Condensed for Auto_AICoding_Harness local templates; no scripts, agents metadata generator, installer, marketplace, or global skill writes included.
---

# Skill Creator

## Purpose

Create or update local project-level skills that are concise, discoverable, auditable, and useful for repeatable engineering work.

## Use When

Use when adding a new `.agents/skills/*/SKILL.md`, consolidating existing skills, adapting a third-party skill, or reviewing whether a skill belongs in this harness.

## Inputs

`AGENTS.md`, `.agents/skills/README.md`, existing `SKILL.md` files, relevant `docs/ai/*`, source or upstream reference notes, license information, and tests that validate generated templates.

## Process

Keep the skill focused on one reusable capability.
Write clear `name` and `description` frontmatter because those control when the skill should trigger.
Include `source`, `upstream`, `license`, and `adaptation_notes` so provenance is auditable.
Keep the body short and procedural: `Purpose`, `Use When`, `Inputs`, `Process`, `Output`, and `Do Not`.
Move detailed project knowledge to `docs/ai/*` instead of duplicating it inside the skill.
Update `.agents/skills/README.md`, generated target structure docs, and tests when the skill set changes.

## Output

A local `SKILL.md` template with clear trigger metadata, bounded instructions, provenance, and matching regression coverage.

## Do Not

Do not add third-party scripts, hooks, installers, marketplace metadata, or global skill writes.
Do not create broad "does everything" skills.
Do not duplicate state-machine or command-contract truth inside a skill.
Do not add a skill without tests that prove it is generated and documented.
