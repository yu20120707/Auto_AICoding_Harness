---
name: skill-creator
description: Use when creating or updating repository-owned global skills, including SKILL.md structure, concise trigger metadata, provenance, installation behavior, and validation checks.
source: adapted
upstream: openai/codex skill-creator
license: see-upstream
adaptation_notes: Expanded for repository-owned harness skills, provenance discipline, and test-backed installation behavior; no marketplace metadata, third-party installers, or plugin logic included.
---

# Skill Creator

## Purpose

Create or update repository-owned global skills that are:

- focused
- discoverable
- auditable
- installable
- testable

This skill prevents the repository from filling up with vague, overlapping, or unmaintainable skill prompts.

## Use When

Use when:

- adding a new `skills/**/SKILL.md`
- expanding a condensed skill into a fuller workflow
- adapting a third-party skill idea
- consolidating several narrow skills into one stronger skill
- reviewing whether a skill belongs in this harness

## Inputs

- `AGENTS.md`
- `skills/README.md`
- existing `SKILL.md` files
- relevant `docs/ai/*`
- source or upstream reference notes
- license information
- installer behavior
- tests that validate global skill installation

## Process

### 1. Confirm the Skill Really Deserves to Exist

A new skill should earn its place.

It should represent:

- one reusable capability
- repeated value across tasks
- a workflow that is hard to remember ad hoc

Do not create a skill for:

- one-off project facts
- one specific bug
- a generic "do everything" prompt

### 2. Choose the Right Scope

A strong skill usually has:

- one core capability
- one clear trigger surface
- bounded inputs
- bounded outputs

If a skill needs two unrelated capabilities, split it.
If three existing skills are tiny and always travel together, consider consolidating them.

### 3. Write Trigger Metadata Carefully

Frontmatter matters because it controls discoverability.

At minimum:

- `name`
- `description`
- `source`
- `upstream`
- `license`
- `adaptation_notes`

The description should say:

- when to use it
- what it helps produce
- why it is different from adjacent skills

### 4. Use a Stable Body Structure

Repository skills should normally include:

- `Purpose`
- `Use When`
- `Inputs`
- `Process`
- `Output`
- `Do Not`

For richer skills, also add:

- overview
- red flags
- verification
- escalation guidance

### 5. Preserve Provenance

If a skill is adapted from upstream:

- keep the source visible
- keep the upstream visible
- keep the license visible
- describe what was changed

Do not present an adapted skill as if it were fully original.

### 6. Respect Installation Behavior

These skills are repository-owned source artifacts.

That means:

- they are not executed by themselves
- they are not installed implicitly by `git clone`
- Codex uses `bin/ai-install-skills` as the example installer
- other tools should use `docs/install-targets.md`

Skill text must not imply hidden installation behavior or secret platform hooks.

### 7. Keep Project Facts Out of Generic Skills

Use `docs/ai/*` for project knowledge.
Use skills for reusable behavior.

Bad pattern:

- embedding repo-specific architecture details in a generic review skill

Good pattern:

- the skill tells the agent to load `docs/ai/*` when needed

### 8. Update Documentation and Tests

When the skill set changes, update:

- `skills/README.md`
- install docs when needed
- generated target structure docs when needed
- tests that validate existence and installation behavior

## Output

Produce a repository-owned `SKILL.md` with:

- clear trigger metadata
- bounded workflow instructions
- explicit provenance
- correct installation behavior
- matching regression coverage

## Do Not

- do not add third-party scripts, hooks, or installers
- do not add marketplace metadata
- do not create broad "does everything" skills
- do not duplicate command-contract or state-machine truth inside a skill
- do not add a skill without updating docs and tests
