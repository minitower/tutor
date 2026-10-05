# Module 6 — Backend Performance: Making It Fast for Real

## Learning objectives
- Measure performance correctly and read the numbers
- Find the actual bottleneck instead of rewriting in a "faster language"
- Know the standard fixes: indexes, caching, queues, scaling

## Lecture outline
1. Latency vs. throughput; percentiles p50/p95/p99; why the average lies
2. Where time really goes: DB and network dominate, CPU rarely; I/O-bound vs. CPU-bound
3. Profiling: py-spy / cProfile, pprof for Go, APM and tracing (OpenTelemetry)
4. Database: indexes, `EXPLAIN ANALYZE`, the N+1 problem, connection pooling (PgBouncer), read replicas
5. Caching: HTTP cache headers, CDN, Redis; cache invalidation and TTL
6. Background jobs and queues: Celery / RQ / Arq, RabbitMQ, Kafka, NATS; what must not happen inside a request
7. Async done right: never block the event loop; when threads or processes are better
8. Scaling: vertical vs. horizontal, stateless services, sessions out of process memory
9. When the language really matters: CPU-heavy work → Go/Rust or a native extension; when it doesn't
10. Load testing with k6 or Locust; honest benchmarks (warm-up, realistic data, same hardware)

## Lab
Load-test the "Slot" API, find the bottleneck, fix it (add an index, cache free slots, move notifications to a queue), re-measure.
- **With an agent:** give the agent the load-test report and `EXPLAIN` output; ask for a hypothesis before any code change; verify the fix with numbers.

## Deliverable
Before/after load-test report with p95 latency and RPS, plus a one-paragraph explanation of the bottleneck.
