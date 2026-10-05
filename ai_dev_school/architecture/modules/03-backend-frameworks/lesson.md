# Module 3 — Backend Languages & Frameworks

## Learning objectives
- Know what a backend does and what every framework gives you
- Know the main backend stacks, their strengths and weaknesses
- Choose a language and framework for a given project and justify it

## Lecture outline
1. What a backend does: routing, validation, auth, business logic, DB access, background jobs, integrations
2. Python
   - FastAPI: async, type hints, auto OpenAPI; best for APIs and AI/ML services
   - Django (+ DRF): "batteries included", admin, ORM; best for content and CRUD-heavy products
   - Flask, Litestar: minimal alternatives
3. Go
   - `net/http` (enough for most services since Go 1.22 routing), Gin, Echo, chi
   - Single binary, goroutines, low memory; best for high-load APIs, infra tools, microservices
4. Node.js / TypeScript: Express, Fastify, NestJS, Hono; one language for front and back, realtime
5. Rust: Axum, Actix Web; max performance and safety, steeper learning curve; hot paths, proxies, CPU-heavy work
6. Java/Kotlin (Spring Boot, Ktor) and C# (ASP.NET Core): enterprise, banks, large teams
7. Concurrency models: GIL + asyncio, goroutines, event loop, Tokio, virtual threads; what "async" actually buys you
8. Data layer: SQL vs. NoSQL, ORM vs. query builder vs. raw SQL, migrations
9. Auth: sessions vs. JWT, OAuth/OIDC, never store passwords in plain text
10. Which stack for which project: MVP, CRUD/admin, high-load API, AI/ML service, realtime, CLI/infra

## Lab
Implement the "Slot" API from the Module 1 OpenAPI in FastAPI with PostgreSQL, migrations and tests. Implement one endpoint again in Go (or Rust) and compare.
- **With an agent:** give the agent the OpenAPI file + test cases and ask it to implement the endpoints test-first; check that it didn't invent fields absent from the contract.

## Deliverable
Working API with migrations and tests + comparison notes (code size, speed of writing, tooling, runtime numbers).
