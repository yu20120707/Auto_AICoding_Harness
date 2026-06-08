# Concurrency Review

## Purpose

Review concurrent code for ownership, synchronization, and lifetime safety.

## Use When

Editing shared state, thread lifetime, mutex or condition_variable logic, atomic usage, or lock ordering.

## Inputs

`docs/ai/concurrency.md`, current diff, thread or crash evidence, and test output.

## Process

Inspect thread lifetime, mutex scope, `condition_variable` usage, lock order, data race and deadlock risk, atomic memory order, shared state boundaries, and object lifetime.

## Output

A concurrency review note or minimal fix plan with explicit locking and ownership reasoning.

## Do Not

Do not introduce shared mutable state without ownership and locking plan.
Do not use relaxed atomics without justification.
