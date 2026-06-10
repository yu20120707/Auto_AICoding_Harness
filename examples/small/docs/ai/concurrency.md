# Concurrency

## Core Rules

- Explain thread lifetime and object lifetime together.
- Identify shared state before changing concurrent code.
- State which lock or atomic protects each shared field.
- Keep lock order explicit and stable.

## Review Points

- thread creation, join, detach, and shutdown behavior
- mutex and condition_variable usage
- lock order and deadlock risk
- data race risk
- atomic memory order assumptions
- callback lifetime versus owning object lifetime

## Required Explanation

When changing concurrent code, explain:

- shared state
- lock protection scope
- lock order
- wakeup conditions
- object lifetime versus thread lifetime

If you cannot explain these clearly, the change is not ready.
