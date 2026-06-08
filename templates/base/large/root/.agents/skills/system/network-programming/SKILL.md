# Network Programming

## Purpose

Keep network code correct across socket lifecycle, framing, retries, and non-blocking behavior.

## Use When

Working on TCP/UDP sockets, partial read/write handling, timeout logic, `epoll`, or protocol framing.

## Inputs

`docs/ai/network.md`, relevant source files, socket logs, timeout settings, and test or repro output.

## Process

Check socket lifecycle, verify TCP/UDP assumptions, account for `EINTR` / `EAGAIN`, handle partial read/write, review non-blocking IO and `epoll` LT/ET behavior, and confirm close / half-close plus packet framing semantics.

## Output

A minimal network-facing implementation or review note with explicit lifecycle and timeout semantics.

## Do Not

Do not assume one read/write completes the message.
Do not change timeout semantics casually.
