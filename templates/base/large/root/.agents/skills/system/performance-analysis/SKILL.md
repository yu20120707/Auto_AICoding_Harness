# Performance Analysis

## Purpose

Ground performance work in baseline and measurement evidence.

## Use When

Investigating latency, throughput, CPU, memory, IO, lock contention, syscall count, or profiling results.

## Inputs

`docs/ai/performance.md`, benchmark output, profiler data, and system measurements.

## Process

Establish a baseline, collect benchmark or profile evidence, compare P50/P95/P99, throughput, CPU, memory, IO, lock contention, and syscall count, then decide whether an optimization is justified.

## Output

A measurement-backed performance note or a bounded optimization plan.

## Do Not

Do not claim performance improvement without measurement.
Do not optimize before baseline.
