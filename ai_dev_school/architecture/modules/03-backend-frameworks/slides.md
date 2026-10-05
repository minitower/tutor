---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 3
## Backend Languages & Frameworks
### Python, Go, Node/TS, Rust, Java/C# — which stack for which project

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- What a backend does and what a framework gives you
- Python: FastAPI, Django
- Go: net/http, Gin, Echo, chi
- Node/TypeScript, Rust, Java/Kotlin, C#
- Concurrency models
- Data: SQL, ORM, migrations
- Auth
- Which stack for which project
- Lab: the "Slot" API

---

<!-- Slide 3 -->
## Learning objectives

- Understand the parts every backend is made of
- Know the main stacks, their strengths and weaknesses
- Understand how languages handle thousands of concurrent requests
- Choose a stack for a project and justify the choice

---

<!-- Slide 4 -->
## What every backend does

1. **Routing** — which code handles `POST /api/bookings`
2. **Validation** — is there a phone, does the slot exist
3. **Authentication and authorization** — who is this and what may they do
4. **Business logic** — you can't book a slot in the past
5. **Data access** — DB, cache
6. **Background jobs** — notifications, reports
7. **Integrations** — Telegram, payments, LLMs

A framework gives you 1–3 and 5; your job is 4.

---

<!-- Slide 5 -->
## Python: FastAPI

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class BookingCreate(BaseModel):
    slot_id: int
    client_name: str
    phone: str

@app.post("/api/bookings", status_code=201)
async def create_booking(data: BookingCreate):
    booking = await book_slot(data)   # business logic
    if booking is None:
        raise HTTPException(409, "slot_taken")
    return booking
```

Types → validation + OpenAPI docs for free. Async. The best choice for APIs and AI/ML services.

---

<!-- Slide 6 -->
## Python: Django

- "Batteries included": ORM, migrations, admin, auth, forms, templates
- **Django Admin** — a ready admin panel in 10 lines of code
- **Django REST Framework** / **Django Ninja** — an API on top
- Best for: content and CRUD products that needed an admin panel "yesterday"
- Less freedom, more conventions — harder for a beginner to get wrong

Alternatives: **Flask** (minimalism), **Litestar** (like FastAPI, more built in)

---

<!-- Slide 7 -->
## Go

```go
func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("POST /api/bookings", createBooking)
    mux.HandleFunc("GET /api/slots/{id}", getSlot)
    log.Fatal(http.ListenAndServe(":8080", mux))
}
```

- Since Go 1.22 the standard `net/http` handles methods and path params — many services need no framework
- **Gin, Echo, chi** — handy middleware, binding, route groups
- A single binary, fast startup, little memory, goroutines
- Best for: high-load APIs, microservices, infra tools (Docker and Kubernetes are written in Go)

---

<!-- Slide 8 -->
## Node.js / TypeScript

| Framework | Character |
|---|---|
| **Express** | The classic, minimal, huge ecosystem |
| **Fastify** | Faster than Express, validation schemas |
| **NestJS** | Angular/Spring-like structure: modules, DI, decorators |
| **Hono** | Lightweight, runs on the edge (Cloudflare Workers, Deno, Bun) |

- One language for front and back, shared types
- Strong at realtime and I/O: chats, WebSocket, proxying other APIs

---

<!-- Slide 9 -->
## Rust

```rust
async fn create_booking(Json(data): Json<BookingCreate>) -> impl IntoResponse {
    match book_slot(data).await {
        Some(b) => (StatusCode::CREATED, Json(b)).into_response(),
        None => (StatusCode::CONFLICT, "slot_taken").into_response(),
    }
}
```

- **Axum**, **Actix Web** — maximum performance, memory safety without a garbage collector
- The compiler catches whole classes of bugs (data races, null)
- The cost: a steep learning curve, slow compilation
- Best for: hot paths, proxies, CPU-heavy work, systems where every millisecond counts

---

<!-- Slide 10 -->
## Java/Kotlin and C#

- **Spring Boot** (Java/Kotlin) — the standard in banks and corporations; a huge ecosystem
- **Ktor** — a lightweight Kotlin framework
- **ASP.NET Core** (C#) — fast, mature, excellent tooling
- Strengths: large teams, long-lived systems, strict types
- Virtual threads (Java 21+) made blocking code cheap

---

<!-- Slide 11 -->
## Concurrency models

How do you serve 10,000 clients all waiting on the database?

| Language | Model | Idea |
|---|---|---|
| Python | GIL + `asyncio` | One Python thread at a time; async switches while waiting on I/O |
| Node.js | Event loop | One thread, all I/O non-blocking |
| Go | Goroutines | Thousands of light threads, the runtime spreads them over cores |
| Rust | Tokio (async) | Like asyncio, but no GIL, on all cores |
| Java | Virtual threads | Write blocking code, the JVM makes it cheap |

---

<!-- Slide 12 -->
## What async actually buys you

- Async speeds up **waiting**, not **computing**
- While a request waits 50 ms for the DB, the process serves other requests
- A heavy computation in an async function **blocks everyone**
- Python: CPU work → separate processes, a queue, or a Rust/C extension
- More on performance in Module 6

---

<!-- Slide 13 -->
## Data: SQL vs NoSQL

| | SQL (PostgreSQL, MySQL) | NoSQL (MongoDB, Redis, DynamoDB) |
|---|---|---|
| Model | Tables and relations | Documents, key-value |
| Guarantees | Transactions, constraints | Depends on the system |
| Schema | Strict, migrations | Flexible |
| When | The default for business data | Cache, sessions, logs, special workloads |

For "Slot": PostgreSQL — relations and double-booking protection (ADR-0002).

---

<!-- Slide 14 -->
## ORM, query builder, SQL

| Approach | Examples | Pros | Cons |
|---|---|---|---|
| ORM | SQLAlchemy, Django ORM, Prisma, GORM | Objects instead of SQL, less code | Hidden slow queries (N+1) |
| Query builder | SQLAlchemy Core, Kysely, sqlc | Control + types | More code |
| Raw SQL | asyncpg, pgx, sqlx | Maximum control and speed | Everything by hand |

**Migrations** (Alembic, Django migrations, goose) — DB schema versions in git, as code.

---

<!-- Slide 15 -->
## Auth

| Approach | How it works | When |
|---|---|---|
| **Sessions** | Session ID in a cookie, data on the server | Classic web apps |
| **JWT** | A signed token with data, held by the client | APIs, mobile clients, microservices |
| **OAuth / OIDC** | "Sign in with Google / Yandex / Telegram" | You don't want to store passwords |

Rules: passwords only as hashes (argon2, bcrypt); short-lived tokens; the **server** checks permissions.

---

<!-- Slide 16 -->
## Which stack for which project

| Project | Recommendation |
|---|---|
| MVP, need it fast | Python (FastAPI/Django) or Node (NestJS) |
| CRUD with an admin panel | **Django** |
| AI/ML service, LLM work | **FastAPI** |
| High-load API | **Go** |
| Realtime: chats, notifications | Node.js or Go |
| Hot path, CPU-heavy | **Rust** |
| Corporation, bank | Java/Kotlin (Spring), C# |

---

<!-- Slide 17 -->
## Benchmarks don't decide

- For 95% of projects the bottleneck is **the DB and the network**, not the language
- Team development speed matters more than language speed
- Ecosystem: are there libraries for your integrations?
- Hiring: whom will you find a year from now?
- Agent familiarity: agents write popular stacks better

> Choose boring technology unless you have a reason not to.

---

<!-- Slide 18 -->
## "Slot" API structure in FastAPI

```
app/
  main.py            # app creation, routers
  api/bookings.py    # endpoints: HTTP only
  services/booking.py# business logic: booking rules
  db/models.py       # tables
  db/repo.py         # DB queries
  schemas.py         # Pydantic: API input and output
migrations/          # Alembic
tests/               # pytest, references to TC-xx
```

Layers: HTTP → logic → data. Logic can be tested without HTTP or a DB.

---

<!-- Slide 19 -->
## Lab

1. Implement the "Slot" API in **FastAPI + PostgreSQL** from the Module 1 OpenAPI
2. Migrations with Alembic, pytest tests from the test cases
3. Double-booking protection — a unique index in the DB
4. Re-implement **one endpoint** in Go (or Rust) — compare
5. **With an agent:** give the agent the OpenAPI + test cases, ask it to implement test-first; check it didn't invent fields absent from the contract

---

<!-- Slide 20 -->
## Deliverable

- A working API with migrations and tests
- The same endpoint in a second language
- Comparison notes: code size, writing speed, tooling, response time, memory
- A list of the agent's "inventions" and how you caught them

---

<!-- Slide 21 -->
## Recap and next module

- Every backend: routing, validation, auth, logic, data, background work
- Python — dev speed and AI; Go — simple performance; Rust — maximum; Node — one language; Java/C# — enterprise
- Async speeds up waiting, not computing
- Next: **Module 4 — API Design**: turning endpoints into an API that is easy and safe to use
