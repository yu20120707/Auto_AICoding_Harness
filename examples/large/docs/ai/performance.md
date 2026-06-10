# Performance

## Evidence First

- Establish a baseline before changing code.
- Record the benchmark or workload used.
- Compare before and after with the same workload.

## Metrics To Watch

- throughput
- latency: P50, P95, P99
- CPU
- memory
- IO
- lock contention
- syscall count
- profile evidence

## Review Rule

Performance optimization is not complete until it shows:

- baseline
- change
- measurement after the change
- regression risk discussion

Do not claim a performance improvement without data.
