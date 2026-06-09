---
name: performance-analysis
description: Ground performance changes in baseline, benchmark, profile evidence, P50/P95/P99, throughput, and resource use.
source: adapted
upstream: addyosmani/agent-skills skills/performance-optimization
license: MIT
adaptation_notes: Expanded into a fuller evidence-first performance workflow for backend and system engineering, not just frontend optimization.
---

# Performance Analysis

## Purpose

Ground performance work in measurement instead of intuition.

This skill exists to prevent:

- premature optimization
- cargo-cult micro-optimizations
- performance claims without baseline evidence

## Use When

Use when:

- performance requirements exist
- a change may affect latency or throughput
- users or monitoring report slowness
- you suspect a regression
- you are touching hot paths, large datasets, or high-concurrency flows

## Inputs

- current behavior or complaint
- baseline timings or metrics
- benchmark or profile output
- current diff
- relevant logs and resource graphs
- test or load commands

## Process

### 1. Measure Before Optimizing

Establish a baseline first.

Prefer concrete measurements such as:

- P50
- P95
- P99
- throughput
- CPU
- memory
- IO wait
- lock contention

If there is no baseline, the first task is measurement.

### 2. Find the Real Bottleneck

Do not optimize what only seems suspicious.

Ask:

- where is time actually spent?
- is the bottleneck CPU, IO, memory, lock contention, network, or allocation churn?
- is the issue local or system-wide?

Use profiles, traces, and benchmarks to answer that question.

### 3. Match the Fix to the Bottleneck

Examples:

- slow query -> query/index/caching work
- contention -> lock scope or concurrency model review
- heavy allocation -> object lifetime or buffering review
- repeated parsing -> cache or data-flow refactor

One bottleneck should lead to one focused hypothesis.

### 4. Measure Again After the Change

After the fix:

- rerun the same benchmark or profile
- compare against the same baseline
- state what improved and by how much
- state what did not improve

### 5. Record Tradeoffs

Performance changes often trade away:

- readability
- memory
- fairness
- correctness margin
- observability

Name the tradeoff explicitly if it exists.

## Metrics To Prefer

Use distribution-aware metrics when possible:

- P50 for normal behavior
- P95/P99 for tail latency
- throughput under realistic load
- peak memory
- CPU saturation point

Average-only reporting is often misleading.

## Verification Pattern

Use a structure like:

```text
baseline:
workload:
measurement_method:
result_before:
result_after:
regression_risk:
```

## Red Flags

- "this should be faster"
- optimization with no benchmark
- reporting only one lucky run
- changing several performance variables at once
- making the code much more complex for negligible gain

## Output

Produce a performance note with:

- baseline
- benchmark or profile evidence
- bottleneck summary
- measured before/after result
- residual risk

## Do Not

- do not optimize before measurement
- do not report performance wins without numbers
- do not rely on average latency alone when tail behavior matters
- do not accept readability or correctness loss without saying so
