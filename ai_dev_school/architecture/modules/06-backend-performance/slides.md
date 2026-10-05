---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 6
## Backend Performance: Making It Fast for Real
### Measure, find the bottleneck, fix it — and measure again

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- Metrics: latency, throughput, percentiles
- Where the time really goes
- Profiling and tracing
- Database: indexes, N+1, connection pooling
- Caching
- Queues and background jobs
- Scaling
- When the language really matters
- Load testing
- Lab

---

<!-- Slide 3 -->
## Learning objectives

- Measure performance correctly and read the numbers
- Find the real bottleneck instead of guessing
- Know the standard fixes: indexes, caching, queues, scaling
- Understand when a rewrite in a "fast language" actually helps

---

<!-- Slide 4 -->
## The main rule

> Don't optimize what you haven't measured.

1. **Measure** — a load test, a profile
2. **Find** the bottleneck — one, the biggest
3. **Fix** it
4. **Measure again** — confirm with numbers

An agent must follow this loop too: hypothesis and data first, code second.

---

<!-- Slide 5 -->
## Latency and throughput

- **Latency** — how long one user waits: ms per request
- **Throughput** — how many requests per second (RPS) the system handles
- Related but not the same: you can serve 10,000 RPS with each one taking 2 seconds
- Under load latency grows: requests start queueing

---

<!-- Slide 6 -->
## Why the average lies

100 requests: 98 at 50 ms, 2 at 5,000 ms

- **Average:** 149 ms — "all good"
- **p50 (median):** 50 ms — half are faster
- **p95:** 50 ms
- **p99:** 5,000 ms — one in a hundred waits 5 seconds

Watch **p95 and p99**: that's the experience of your unhappiest users. An active user makes dozens of requests per session and will almost certainly hit the tail.

---

<!-- Slide 7 -->
## Where the time really goes

A typical request to the "Slot" API:

| Stage | Time |
|---|---|
| Parsing, validation | 0.2 ms |
| Business logic in Python | 1 ms |
| **DB query without an index** | **180 ms** |
| External API call (Telegram) | **300 ms** |
| Response serialization | 0.5 ms |

Language — 1.7 ms. DB and network — 480 ms. A Rust rewrite would save ~1 ms.

---

<!-- Slide 8 -->
## I/O-bound vs CPU-bound

| | I/O-bound | CPU-bound |
|---|---|---|
| Where the time goes | Waiting on DB, network, disk | Computing: images, reports, crypto, ML |
| Share of web APIs | The vast majority | Rare endpoints |
| What helps | Async, caching, indexes, queues | Better algorithm, processes, Go/Rust, GPU |

Figure out which case you have first — the fixes are opposite.

---

<!-- Slide 9 -->
## Profiling and tracing

- **Profiler** — where the process spends time: py-spy, cProfile (Python), pprof (Go)
- **Flame graph** — bar width = share of time; look for the widest
- **Tracing (OpenTelemetry)** — one request's path through all services and the DB, with timings
- **APM** (Grafana, Sentry, Datadog) — slow requests and endpoints in production
- **Slow query log** in PostgreSQL: `log_min_duration_statement`

---

<!-- Slide 10 -->
## DB: indexes and EXPLAIN

```sql
EXPLAIN ANALYZE
SELECT * FROM slots WHERE master_id = 7 AND starts_at > now() AND NOT booked;

-- without an index:
Seq Scan on slots  (actual time=0.02..182.4 rows=12)
  Rows Removed by Filter: 1999988

-- after CREATE INDEX ON slots (master_id, starts_at) WHERE NOT booked:
Index Scan using slots_master_starts_idx  (actual time=0.03..0.09 rows=12)
```

A Seq Scan over a big table in a hot query is suspect number one.

---

<!-- Slide 11 -->
## The N+1 problem

```python
masters = session.query(Master).all()          # 1 query
for m in masters:
    print(m.name, len(m.slots))                # + N queries, one per master
```

100 masters = 101 queries. Each is fast, together they take a second.

```python
masters = session.query(Master).options(selectinload(Master.slots)).all()  # 2 queries
```

ORMs hide queries — turn on SQL logging in development.

---

<!-- Slide 12 -->
## Connection pooling and replicas

- Opening a PostgreSQL connection is expensive (tens of ms, memory on the server)
- A **connection pool** reuses open connections (built into SQLAlchemy, pgx; external — PgBouncer)
- Too many connections — the DB spends memory on them instead of data
- **Read replicas** — DB copies for SELECTs when the primary can't keep up

---

<!-- Slide 13 -->
## Caching: the layers

| Layer | What we cache | Tool |
|---|---|---|
| Browser | Static files, API responses | `Cache-Control`, `ETag` |
| CDN | Images, JS, CSS, public pages | Cloudflare, a cloud CDN |
| Application | Results of expensive queries | Redis, Memcached |
| Database | Hot data in memory | PostgreSQL buffers |

---

<!-- Slide 14 -->
## App-level cache: cache-aside

```python
async def free_slots(master_id: int):
    key = f"free_slots:{master_id}"
    if cached := await redis.get(key):
        return json.loads(cached)
    slots = await repo.free_slots(master_id)
    await redis.set(key, json.dumps(slots), ex=30)   # TTL 30 seconds
    return slots

# on booking a slot:
await redis.delete(f"free_slots:{master_id}")        # invalidation
```

Two hard parts: **invalidation** (when data is stale) and **TTL** (how long stale is acceptable).

---

<!-- Slide 15 -->
## Queues and background jobs

Don't do inside a request what the user isn't waiting for:

- Sending Telegram and e-mail notifications
- Generating reports and PDFs
- Processing images
- LLM calls that take minutes

```
API → puts a job in the queue → responds 201 immediately
Worker → takes the job → sends the notification → retries on failure
```

Tools: Celery, RQ, Arq (Python) · RabbitMQ, Redis · Kafka, NATS — for event streams

---

<!-- Slide 16 -->
## Scaling

| | Vertical | Horizontal |
|---|---|---|
| How | More CPU and RAM on one server | More app copies behind a load balancer |
| Easy? | Very — change the plan | Needs stateless code |
| Limit | The biggest server available | Almost none (except the DB) |

**Stateless:** the app keeps nothing between requests in process memory. Sessions, files, cache go to Redis, S3, the DB.

---

<!-- Slide 17 -->
## When the language really matters

- CPU work: image and video processing, cryptography, parsing huge files, simulations
- Huge RPS with thin logic: proxies, gateways, exchanges
- Hard memory and latency limits: p99 < 5 ms
- Fixes: move the hot path into a Go/Rust service, a Rust extension for Python (PyO3), ready native libraries (NumPy, Polars)

You rewrite the **hot path**, not the whole app.

---

<!-- Slide 18 -->
## Load testing

```js
// k6: load.js
import http from 'k6/http';
export const options = { vus: 50, duration: '1m' };
export default function () {
  http.get('https://staging.slot.example/api/masters/7/slots');
}
```

```
http_req_duration: avg=212ms p(95)=480ms p(99)=1.2s
http_reqs: 13 820   230/s
```

The Python alternative — **Locust**.

---

<!-- Slide 19 -->
## Honest benchmarks

- **Warm-up:** the first requests are slower (caches, JIT, connection pool)
- **Realistic data:** 10 rows in the DB are always fast — test with millions
- **Same hardware** and the same settings
- **A realistic scenario:** not just a GET of one page
- **The load generator** runs on a different machine than the app
- Compare p95/p99, not the average

---

<!-- Slide 20 -->
## Lab

1. Fill the "Slot" DB with realistic data: 1,000 masters, 2 million slots
2. Run a k6 or Locust load test: record p95 and RPS
3. Find the bottleneck: `EXPLAIN ANALYZE`, a profiler, SQL logs
4. Fix it: an index, a cache for free slots, notifications in a queue
5. Measure again
6. **With an agent:** give the agent the test report and the `EXPLAIN` output; ask for a hypothesis before code; confirm the fix with numbers

---

<!-- Slide 21 -->
## Deliverable

- A before/after report: p50, p95, p99, RPS
- A paragraph: what the bottleneck was and how you proved it
- The load-test script in the repo
- Where the agent guessed right, and where it proposed an optimization without data

---

<!-- Slide 22 -->
## Recap and next module

- Measure → find → fix → measure again
- Watch p95/p99, not the average
- Usually the DB and the network are to blame: indexes, N+1, caching, queues
- Horizontal scaling needs stateless code
- Next: **Module 7 — AI Inside the App**: adding an LLM to "Slot" — the slowest and most expensive dependency of all
