# Module 5 — Databases: Model, Transactions, Scale

## Learning objectives
- Model data so the database itself enforces the business rules
- Understand transactions and isolation, and prevent race conditions like double booking
- Change the schema of a live database without downtime
- Choose the right storage for each kind of data and know the order in which to scale it

## Lecture outline
1. Why the database is the heart of the app: data outlives code; data mistakes are the most expensive
2. Data modeling: entities and relations, keys, normalization and when to denormalize
3. Constraints as business rules: `NOT NULL`, `CHECK`, `UNIQUE`, foreign keys, partial unique indexes, `EXCLUDE` for overlapping time ranges
4. Transactions and ACID
5. Race conditions: check-then-insert, lost updates; fixes — constraints, conditional `UPDATE`, `SELECT … FOR UPDATE`
6. Isolation levels in PostgreSQL: Read Committed, Repeatable Read, Serializable; anomalies and retries
7. Indexes in depth: B-tree and column order, partial, covering, GIN/GiST; the write cost of indexes
8. Zero-downtime migrations: expand → migrate → contract; dangerous operations and `CREATE INDEX CONCURRENTLY`
9. JSONB: when semi-structured data in PostgreSQL is fine
10. Choosing storage: PostgreSQL by default; Redis, MongoDB, ClickHouse, search engines, object storage, vector search
11. OLTP vs OLAP: don't run analytics on the production database
12. Scaling order: queries and indexes → vertical → pooling → read replicas (and replication lag) → caching → partitioning → sharding
13. Backups and point-in-time recovery (WAL)
14. Databases and AI agents: read-only roles, reviewed migrations, never production write access

## Lab
Rebuild the "Slot" schema with constraints that make double booking impossible (partial unique index, `EXCLUDE` for overlapping slots). Write a test that fires 50 concurrent bookings for one slot and proves exactly one succeeds. Perform one zero-downtime migration (expand → migrate → contract) while a load test runs.
- **With an agent:** ask the agent to propose the schema from the ER diagram in Module 1 and to write the concurrency test; check every constraint it suggests by trying to break it.

## Deliverable
Migrations, the concurrency test (green), a log of the zero-downtime migration with zero failed requests, and an ADR on storage choices.
