---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 5
## Databases: Model, Transactions, Scale
### Making double booking impossible — at the level of the database itself

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- Why the database is the heart of the app
- Data modeling and constraints
- Transactions, race conditions, isolation levels
- Indexes in depth
- Zero-downtime migrations
- JSONB and choosing storage
- OLTP vs OLAP
- The order of scaling
- Backups and recovery
- Lab

---

<!-- Slide 3 -->
## Learning objectives

- Model data so **the database itself enforces the business rules**
- Understand transactions and isolation, and prevent race conditions
- Change the schema of a live database **without downtime**
- Choose storage for the data and know the order of scaling

---

<!-- Slide 4 -->
## Why the database is the heart of the app

- Code gets rewritten every couple of years; data lives for **decades** and outlives several app versions
- A code bug is fixed by a deploy; corrupted data sometimes **can't be fixed at all**
- The API, workers, admin panel, analytics and scripts all touch one DB — a rule in one of them doesn't protect against the others
- Most performance problems are in the DB (Module 6)

> The database is the last line of defense. What it doesn't forbid will eventually happen.

---

<!-- Slide 5 -->
## Data modeling

- **Entities → tables**, relations → foreign keys (from the Module 1 ER diagram)
- **Keys:** a surrogate key (`id bigint`) by default; a natural key (phone, email) changes — don't make it primary
- **Normalization:** every fact is stored in one place — no contradictions on update
- **Denormalization** — deliberately, for read speed, with a clear way to keep the copy current
- Time is always `timestamptz`; money is `numeric` or an integer in kopecks, never `float`

---

<!-- Slide 6 -->
## The "Slot" schema

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE masters (
  id        bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name      text NOT NULL,
  timezone  text NOT NULL DEFAULT 'Europe/Moscow'
);

CREATE TABLE slots (
  id         bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  master_id  bigint NOT NULL REFERENCES masters(id),
  starts_at  timestamptz NOT NULL,
  ends_at    timestamptz NOT NULL CHECK (ends_at > starts_at),
  booked     boolean NOT NULL DEFAULT false,
  EXCLUDE USING gist (master_id WITH =, tstzrange(starts_at, ends_at) WITH &&)
);

CREATE TABLE bookings (
  id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  slot_id       bigint NOT NULL REFERENCES slots(id),
  client_phone  text NOT NULL CHECK (client_phone ~ '^\+7[0-9]{10}$'),
  status        text NOT NULL DEFAULT 'confirmed'
                CHECK (status IN ('confirmed', 'cancelled', 'done', 'no_show')),
  created_at    timestamptz NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX one_active_booking_per_slot
  ON bookings (slot_id) WHERE status <> 'cancelled';
```

---

<!-- Slide 7 -->
## Constraints as business rules

| Business rule | DB constraint |
|---|---|
| A slot has a barber | `REFERENCES masters(id)` |
| A slot ends after it starts | `CHECK (ends_at > starts_at)` |
| A barber's slots don't overlap | `EXCLUDE USING gist (... WITH &&)` |
| The phone has the right format | `CHECK (client_phone ~ ...)` |
| At most one active booking per slot | A partial `UNIQUE ... WHERE status <> 'cancelled'` |
| Status comes from a list | `CHECK (status IN (...))` |

The partial index matters: a plain `UNIQUE (slot_id)` would forbid booking a slot again after a cancellation.

---

<!-- Slide 8 -->
## Transactions and ACID

- **Atomicity** — all or nothing: the booking is created **and** the slot is marked taken, or neither
- **Consistency** — after the transaction every constraint holds
- **Isolation** — concurrent transactions don't see each other's "halves"
- **Durability** — what was committed survives a server crash (WAL on disk)

```python
async with db.transaction():
    await mark_slot_booked(slot_id)
    booking = await insert_booking(slot_id, phone)
    await enqueue_notification(booking.id)   # an outbox table in the same transaction
```

---

<!-- Slide 9 -->
## The race: "check, then insert"

```python
if not await repo.slot_is_free(slot_id):      # both clients see "free"
    raise SlotTaken()
await repo.insert_booking(slot_id, phone)     # both insert → double booking
```

| Time | Client A | Client B |
|---|---|---|
| 14:03:00.001 | Slot free? — yes | |
| 14:03:00.002 | | Slot free? — yes |
| 14:03:00.003 | Insert booking | |
| 14:03:00.004 | | Insert booking |

You can't reproduce this bug on a laptop with one user. On a launch with a discount it happens in the first hour.

---

<!-- Slide 10 -->
## Closing the race

**1. A DB constraint + error handling** — the most reliable option:

```python
try:
    await repo.insert_booking(slot_id, phone)
except IntegrityError:            # one_active_booking_per_slot fired
    raise SlotTaken()             # → 409 Conflict
```

**2. A conditional UPDATE** — an atomic "check and write" in one statement:

```sql
UPDATE slots SET booked = true WHERE id = 42 AND NOT booked RETURNING id;
-- 0 rows → the slot is already taken
```

**3. A row lock** — `SELECT ... FROM slots WHERE id = 42 FOR UPDATE` inside a transaction: the second client waits until the first one finishes.

---

<!-- Slide 11 -->
## Isolation levels in PostgreSQL

| Level | Guarantee | Cost |
|---|---|---|
| **Read Committed** (default) | Only committed data is visible; each statement sees a fresh snapshot | Lost updates and check-then-insert races are possible |
| **Repeatable Read** | The whole transaction sees one snapshot | A write conflict → an error, needs a retry |
| **Serializable** | As if transactions ran strictly one by one | More serialization failures → the code must retry the transaction |

In practice: Read Committed + constraints + conditional UPDATEs solve most problems. Serializable is for complex invariants across many rows, and only with a retry loop.

---

<!-- Slide 12 -->
## Indexes in depth

- **B-tree** — the default: equality, ranges, sorting
- A **composite index** `(master_id, starts_at)` works for `master_id = 7` and for `master_id = 7 AND starts_at > now()`, but **not** for `starts_at` alone — column order matters
- **Partial** `WHERE NOT booked` — smaller and faster if you only look for free slots
- **Covering** `INCLUDE (ends_at)` — the answer comes from the index without reading the table
- **GIN** — JSONB, full-text search, arrays; **GiST** — ranges, geodata
- Every index **slows down writes** and takes space; find unused ones in `pg_stat_user_indexes`

---

<!-- Slide 13 -->
## Zero-downtime migrations: expand → migrate → contract

Rename `client_phone` → `phone` without stopping the service:

1. **Expand:** add a `phone` column; new code writes to **both** columns
2. **Migrate:** copy old data in batches (`UPDATE ... WHERE id BETWEEN ...`)
3. **Switch:** the code reads from `phone`
4. **Contract:** the code stops writing `client_phone`; in the next release, drop the column

Every step is compatible with both the old and the new code version — both run during a deploy.

---

<!-- Slide 14 -->
## Dangerous operations in migrations

| Operation | Problem | Safe way |
|---|---|---|
| `CREATE INDEX` | Blocks writes to the table while it builds | `CREATE INDEX CONCURRENTLY` |
| `ALTER COLUMN ... TYPE` | Rewrites the whole table under a lock | A new column + data copy |
| `SET NOT NULL` on a big table | A full scan under a lock | `CHECK (...) NOT VALID`, then `VALIDATE CONSTRAINT` |
| Any `ALTER TABLE` | Waits for a lock and queues every query behind it | `SET lock_timeout = '3s'` and retry |

Rule: run a migration on a big table against a copy of production data first.

---

<!-- Slide 15 -->
## JSONB: flexibility inside PostgreSQL

```sql
ALTER TABLE masters ADD COLUMN settings jsonb NOT NULL DEFAULT '{}';
SELECT * FROM masters WHERE settings @> '{"reminders": {"sms": true}}';
CREATE INDEX ON masters USING gin (settings);
```

- **Good for:** settings, external API responses, rare optional attributes
- **Bad for:** anything you search, sort or join on — those are columns
- JSONB often covers the "we need MongoDB" need

---

<!-- Slide 16 -->
## Choosing storage

| Data | Storage |
|---|---|
| Business data, relations, transactions | **PostgreSQL** — the default |
| Cache, sessions, queues, counters, rate limits | **Redis** / Valkey |
| Documents with very different shapes | MongoDB — or JSONB in PostgreSQL |
| Analytics, events, logs, billions of rows | **ClickHouse** |
| Full-text search with morphology, facets | OpenSearch / Elasticsearch, Meilisearch |
| Files, images, backups | **Object storage (S3)** — not a DB |
| Vectors for semantic search | **pgvector** in PostgreSQL, Qdrant (Module 7) |

Every new store is one more system to back up, upgrade and monitor.

---

<!-- Slide 17 -->
## OLTP vs OLAP

| | OLTP | OLAP |
|---|---|---|
| Example | "Book a client into a slot" | "Conversion per barber for the quarter" |
| Queries | Many short ones, by key | Few heavy ones, over whole tables |
| Storage | PostgreSQL | ClickHouse, a data warehouse |
| Layout | Row-oriented | Column-oriented |

A heavy analytical query on the production DB slows down client bookings. Analytics goes to a replica or a separate columnar store.

---

<!-- Slide 18 -->
## The order of scaling

1. **Queries and indexes** — `EXPLAIN ANALYZE` (Module 6); most often this is enough
2. **Vertical** — more CPU, memory, fast disks
3. **Connection pooling** — PgBouncer
4. **Read replicas** — watch **replication lag**: the client booked, but the replica doesn't know yet — read fresh data from the primary
5. A **cache** in front of the DB — Redis
6. **Partitioning** — big tables by time (slots by month)
7. **Sharding** — data across several servers; the hardest and the last resort

Each step costs more to maintain — don't skip steps.

---

<!-- Slide 19 -->
## Backups and point-in-time recovery

- `pg_dump` — a logical copy; simple, but slow to restore on big DBs
- **Physical backup + WAL archive** (pgBackRest, WAL-G) → **PITR**: restore to 14:02:59, a second before the mistaken `DELETE`
- Managed cloud DBs do this for you — check how many days back
- Regular **test restores** are part of the process (Module 11)

---

<!-- Slide 20 -->
## Databases and AI agents

- Give an agent a **read-only role** and a copy of the data without personal information (MCP to a DB is covered in the agents course)
- Migrations written by an agent go through review and a run on a data copy
- Agents like to "simplify" a schema by dropping an inconvenient constraint — the constraint is the protection
- Never write access to the production DB

---

<!-- Slide 21 -->
## Lab

1. Rebuild the "Slot" schema: foreign keys, `CHECK`, `EXCLUDE` for overlapping slots, a partial unique index on the active booking
2. A test: 50 concurrent bookings for one slot → **exactly one** succeeds, the rest get 409
3. A zero-downtime migration (expand → migrate → contract) during a load test — zero failed requests
4. Check the indexes with `EXPLAIN ANALYZE`
5. **With an agent:** ask the agent to propose the schema from the ER diagram and write the concurrency test; check every constraint by trying to break it

---

<!-- Slide 22 -->
## Deliverable

- Schema migrations in the repo
- A green concurrency test
- A log of the zero-downtime migration: zero errors under load
- An ADR on the storage choices for "Slot"

---

<!-- Slide 23 -->
## Recap and next module

- Business rules live in DB constraints, not only in code
- Races are closed by constraints, conditional UPDATEs and locks, not by checks in code
- Migrations: expand → migrate → contract
- PostgreSQL by default; a new store only for a real need
- Next: **Module 6 — Backend Performance**: measuring and finding the bottleneck
