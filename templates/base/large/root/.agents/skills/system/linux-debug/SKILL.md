# Linux Debug

## Purpose

Drive Linux issue analysis from system evidence instead of guesswork.

## Use When

Investigating crashes, hangs, permission failures, fd leaks, process state issues, or environment-specific Linux behavior.

## Inputs

`docs/ai/linux-debug.md`, logs, `strace`, `gdb`, core dump data, `/proc`, `lsof`, `ss`, `dmesg`, `journalctl`, and permission context.

## Process

Collect logs, inspect process and fd/process state, use `strace` / `gdb` / core dump evidence, check `/proc`, `lsof`, `ss`, `dmesg`, and `journalctl`, then narrow the issue to a concrete cause.

## Output

An evidence-backed Linux debugging note or minimal fix plan.

## Do Not

Do not guess without logs or system evidence.
Do not run destructive commands.
