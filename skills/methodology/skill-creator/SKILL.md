---
name: skill-creator
description: Use when creating or updating repository-owned global skills, including SKILL.md structure, concise trigger metadata, provenance, installation behavior, and validation checks.
source: adapted
upstream: openai/codex skill-creator
license: see-upstream
adaptation_notes: Condensed for Auto_AICoding_Harness repository-owned global skills; no third-party scripts, agents metadata generator, or marketplace metadata included.
---

# Skill Creator

## Purpose

Create or update repository-owned global skills that are concise, discoverable, auditable, and useful for repeatable engineering work.

## Use When

Use when adding a new `skills/**/SKILL.md`, consolidating existing skills, adapting a third-party skill idea, or reviewing whether a skill belongs in this harness.

## Inputs

`AGENTS.md`, `skills/README.md`, existing `SKILL.md` files, relevant `docs/ai/*`, source or upstream reference notes, license information, installer behavior, and tests that validate global skill installation.

## Process

Keep the skill focused on one reusable capability.
Write clear `name` and `description` frontmatter because those control when the skill should trigger.
Include `source`, `upstream`, `license`, and `adaptation_notes` so provenance is auditable.
Keep the body short and procedural: `Purpose`, `Use When`, `Inputs`, `Process`, `Output`, and `Do Not`.
Move detailed project knowledge to `docs/ai/*` instead of duplicating it inside the skill.
Update `skills/README.md`, install docs, generated target structure docs, and tests when the skill set changes.

## Output

A repository-owned `SKILL.md` with clear trigger metadata, bounded instructions, provenance, installability, and matching regression coverage.

## Do Not

Do not add third-party scripts, hooks, installers, marketplace metadata, or global skill writes.
Do not create broad "does everything" skills.
Do not duplicate state-machine or command-contract truth inside a skill.
Do not add a skill without tests that prove it is generated and documented.
