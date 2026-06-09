---
name: repo-onboarding-analysis
description: Analyze an unfamiliar repository or subsystem before changes. Use when the user asks to understand a repo, map architecture, find entry points, prepare onboarding or handoff docs, or decide where future changes should go. Produces evidence-backed, read-only onboarding and architecture artifacts.
source: adapted
upstream: notque/claude-code-toolkit codebase-overview; affaan-m/ECC codebase-onboarding; hoangsonww/Claude-Code-Agent-Monitor repo-onboarding; addyosmani/agent-skills source-driven-development
license: see-upstream
adaptation_notes: Expanded into a fuller repository-owned onboarding workflow for Auto_AICoding_Harness; remains instruction-only and does not vendor third-party scripts or force writes by default.
---

# Repo Onboarding Analysis

## Purpose

Create durable repository knowledge before an agent starts changing an existing project.

The goal is to keep:

- global instructions thin
- repository `AGENTS.md` thin
- project facts explicit and evidence-backed inside `docs/ai/*`

## Use When

Use this skill when:

- entering an existing repository
- `docs/ai/*` is missing or stale
- starting medium or complex work in an unfamiliar codebase
- the user asks for architecture, module, build, test, or risk documentation
- the agent needs to decide where future changes should go

## Inputs

- `AGENTS.md`
- `README.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- existing `docs/ai/*`
- build files
- package manifests
- CI files
- scripts
- source tree
- tests
- recent git history when useful

## Process

### 1. Detect the Repository Frame

Identify:

- repository root
- active language stack
- build system
- test entrypoints
- CI workflows
- generated or ignored directories
- existing AI-facing docs

Do this before reading source deeply.

### 2. Build a Bounded File Map

Use fast discovery first:

- manifests
- top-level directories
- CI files
- scripts
- primary package or build definitions

Only then move into source.
The first pass should answer:

- where code lives
- where tests live
- where integration boundaries exist
- where deploy/build logic lives

### 3. Find Entrypoints and Major Modules

Map:

- application entrypoints
- service boundaries
- worker/CLI/background jobs
- public APIs or protocols
- persistence layers
- config surfaces
- external dependencies

Do not describe architecture as "MVC", "clean architecture", or similar labels unless files actually support that claim.

### 4. Trace Critical Flows

For important workflows, capture:

- request entrypoint
- key handlers
- business logic modules
- persistence/external call sites
- emitted side effects

Typical flows:

- startup
- request processing
- background processing
- persistence write path
- authentication or permissions

### 5. Derive Real Build And Test Commands

Use only commands supported by files that exist:

- `package.json`
- `Makefile`
- `CMakeLists.txt`
- CI workflow files
- checked-in scripts

If a command is inferred rather than proven, mark it unknown.
Do not present guessed commands as fact.

### 6. Produce Evidence-Backed Notes

Every important claim should be traceable to:

- file paths
- command output
- config entries
- scripts

If an architecture claim cannot be tied back to evidence, soften it or remove it.

### 7. Place Knowledge in the Right Layer

Project facts belong in `docs/ai/*`.

Good examples:

- `docs/ai/repo-map.md`
- `docs/ai/architecture-map.md`
- `docs/ai/build-and-test.md`
- `docs/ai/risk-map.md`

Do not turn `AGENTS.md` into a long architecture dump.

### 8. Capture Unknowns Explicitly

A good onboarding artifact includes what is still unclear:

- missing commands
- unverified flows
- suspicious dead zones
- unknown ownership areas
- risky modules needing later review

## Output

Default output is a conversational onboarding analysis.

If the user asks to write artifacts, produce or update:

- `docs/ai/repo-onboarding.md`
- `docs/ai/repo-map.md`
- `docs/ai/architecture-map.md`
- `docs/ai/build-and-test.md`
- `docs/ai/risk-map.md`
- `docs/ai/agent-handoff.md`

The output should include:

- repository overview
- boundaries and non-goals
- technology stack
- module map
- entrypoints
- critical flows
- build/test commands
- where future changes should go
- risk map
- unknowns
- evidence paths

Repo onboarding should be read-only unless the user explicitly asked to materialize docs.

## Red Flags

- writing code before understanding the repo shape
- copying README claims without checking files
- guessing commands
- documenting the whole tree without explaining which paths matter
- mixing project facts into global instructions
- dumping raw source into onboarding docs

## Do Not

- do not implement code, fix bugs, or refactor while onboarding
- do not dump full source listings into docs
- do not write repository facts into global `AGENTS.md`
- do not write files by default; write artifacts only when the user asks
- do not overwrite existing project docs without safe-write or explicit approval
- do not install dependencies, run heavy services, or execute destructive commands
- do not claim architecture facts that were not verified from files or commands
- do not read or print secret values from `.env*`, credential, token, key, or private config files
