# Syllabus

Each module: **Objectives → Key concepts → Lab → Deliverable**. Full detail
lives in `modules/<module-name>/lesson.md` (English) and `lesson.ru.md`
(Russian). Every lab extends the running project "Slot" (see
[README.md](README.md)).

---

## Module 0 — The Big Picture: How a Modern Application Works
- Objectives: explain what frontend, backend and infrastructure are, how
  they talk to each other, and why each layer uses the languages it does
- Key concepts: client–server model; the life of a request (URL → DNS →
  TCP/TLS → CDN → load balancer / reverse proxy → API → database → back);
  HTTP, REST, JSON, WebSocket, gRPC; why the browser runs only
  HTML/CSS/JS (+ WebAssembly) and TypeScript compiles to JS; why the
  backend can be any language; infrastructure as code (YAML, HCL, Bash);
  monolith vs. microservices vs. modular monolith; where AI/LLM calls sit
- Lab: open DevTools on a real site, trace one page load (DNS, requests,
  API calls, timings), draw the architecture you can infer
- Deliverable: annotated request trace + a first block diagram of "Slot"

## Module 1 — Project Documentation: From Idea to Spec
- Objectives: describe a product so a developer, a tester and an AI agent
  all build the same thing
- Key concepts: vision / PRD; user story (`As a… I want… so that…`) +
  acceptance criteria (Given/When/Then); use case (actors, main and
  alternative flows); test case; BPMN (events, tasks, gateways, lanes);
  UML (use case, sequence, class, state, ER) and C4 (context → container
  → component); ADR; API contract (OpenAPI); docs-as-code (Mermaid,
  PlantUML, BPMN XML in the repo); how agents read docs: text over
  pictures, diagrams as code, `AGENTS.md`/`CLAUDE.md`, linking specs to
  tests
- Lab: write the "Slot" spec: 8–10 user stories, 2 use cases, the booking
  BPMN, a C4 container diagram, an ER diagram, an OpenAPI draft, test
  cases; give it to an agent and ask it to find gaps
- Deliverable: `docs/` folder with all artifacts + list of gaps the agent
  found and how you fixed them

## Module 2 — Frontend Frameworks: How to Choose
- Objectives: understand how a modern frontend works and pick a framework
  for a task with arguments, not hype
- Key concepts: DOM, components, state, reactivity (virtual DOM vs.
  signals vs. compiler); rendering strategies: SPA, SSR, SSG, ISR,
  islands, hydration, React Server Components; React, Vue, Angular,
  Svelte, Solid; meta-frameworks: Next.js, Nuxt, SvelteKit, Astro,
  React Router (ex-Remix); tooling: Vite, npm/pnpm, TypeScript; styling:
  CSS modules, Tailwind, component libraries; beyond the browser: React
  Native, Flutter, Tauri/Electron; decision matrix (SEO need,
  interactivity, team, ecosystem, hiring)
- Lab: build the "Slot" public page (SSR/SSG for SEO) and the admin panel
  (SPA) against a mock API; run Lighthouse on both
- Deliverable: two frontends + Lighthouse reports + a one-page ADR
  "why this framework"

## Module 3 — Backend Languages & Frameworks
- Objectives: know the main backend stacks, their strengths, and which
  project each fits
- Key concepts: what a backend does (routing, validation, auth, business
  logic, DB access, background jobs); Python: FastAPI, Django (+DRF),
  Flask/Litestar; Go: `net/http`, Gin, Echo, chi; Node/TypeScript:
  Express, Fastify, NestJS, Hono; Rust: Axum, Actix Web; Java/Kotlin:
  Spring Boot, Ktor; C#: ASP.NET Core; concurrency models (GIL + asyncio,
  goroutines, event loop, Tokio, virtual threads); ORMs and migrations;
  auth (sessions, JWT, OAuth); which stack for which project: MVP,
  admin-heavy CRUD, high-load API, AI/ML service, realtime
- Lab: implement the "Slot" API from the Module 1 OpenAPI in FastAPI;
  implement one endpoint again in Go (or Rust); compare
- Deliverable: working API with migrations and tests + comparison notes

## Module 4 — API Design: A Contract People and Agents Can Rely On
- Objectives: design an API whose behavior clients can predict, that
  survives retries and concurrent edits, and that evolves without breaking
  clients
- Key concepts: resources and URLs; safe and idempotent methods; the status
  codes that matter; one error format (Problem Details, RFC 9457);
  validation with field-level errors; offset vs cursor pagination;
  conventions for dates and money; `Idempotency-Key`; ETag and `If-Match`
  (optimistic locking); additive vs breaking changes, `Deprecation` and
  `Sunset`; scopes and rate limits; signed webhooks; REST vs GraphQL vs
  gRPC vs SSE; contract-first with Spectral, Prism and Schemathesis; APIs
  designed for AI agents
- Lab: revise the "Slot" OpenAPI (errors, cursor pagination, idempotent
  booking, ETag, a signed webhook), implement it, lint with Spectral, run
  Schemathesis
- Deliverable: `openapi.yaml` passing Spectral + implementation +
  Schemathesis report + versioning ADR

## Module 5 — Databases: Model, Transactions, Scale
- Objectives: make the database enforce the business rules, prevent race
  conditions, change a live schema without downtime, choose storage well
- Key concepts: data modeling and keys; constraints as business rules
  (`CHECK`, foreign keys, partial unique indexes, `EXCLUDE` for overlapping
  time ranges); ACID; check-then-insert races and their fixes (constraints,
  conditional `UPDATE`, `SELECT … FOR UPDATE`); PostgreSQL isolation
  levels; index types and column order; expand → migrate → contract and
  dangerous migration operations; JSONB; choosing storage (Redis,
  ClickHouse, search, S3, pgvector); OLTP vs OLAP; the order of scaling;
  PITR backups; databases and AI agents
- Lab: rebuild the "Slot" schema with constraints that make double
  booking impossible; prove it with 50 concurrent bookings; run a
  zero-downtime migration under load
- Deliverable: migrations + green concurrency test + migration log with
  zero failed requests + storage ADR

## Module 6 — Backend Performance: Making It Fast for Real
- Objectives: find the actual bottleneck and fix it, instead of
  rewriting in a "faster language"
- Key concepts: latency vs. throughput, p50/p95/p99; where time really
  goes (DB, network, I/O vs. CPU); profiling; DB: indexes, `EXPLAIN`,
  N+1, connection pooling; caching (HTTP cache, CDN, Redis); background
  jobs and queues (Celery/RQ/Arq, RabbitMQ, Kafka, NATS); async done
  right; horizontal vs. vertical scaling, stateless services; when the
  language really matters (CPU-bound work → Go/Rust); load testing
  (k6, Locust); honest benchmarks
- Lab: load-test the "Slot" API, find the bottleneck, fix it (index /
  cache / queue for notifications), re-measure
- Deliverable: before/after load-test report with p95 and RPS

## Module 7 — AI Inside the App: LLMs as Part of the Architecture
- Objectives: treat an LLM as an architectural dependency and build a
  safe, affordable, measurable AI feature
- Key concepts: latency, per-token cost, non-determinism, refusals;
  single call vs workflow vs agent; request anatomy and `usage`; cost
  estimates and prompt caching; streaming over SSE; structured outputs;
  tool use and the tool loop; RAG with pgvector, and when the data simply
  fits in the context; backend-only keys, timeouts, per-user limits and
  budgets; `stop_reason` handling, fallbacks, graceful degradation; prompt
  injection and least-privilege tools; evals; cost and latency tracking
- Lab: an AI booking assistant for "Slot" (intent → find slots → human
  confirmation), streamed over SSE, with a cached price list/FAQ, limits,
  and a 30-case eval set; then try to break it with prompt injection
- Deliverable: assistant endpoint + eval results (accuracy, cost, latency)
  + monthly cost estimate + prompt-injection threat note

## Module 8 — Docker: Packaging the Application
- Objectives: understand what a container is under the hood and package
  "Slot" so it runs the same everywhere
- Key concepts: "works on my machine"; VM vs. container; namespaces,
  cgroups, layered filesystem; image, layer, container, registry; Docker
  architecture (CLI → daemon → containerd → runc); Dockerfile, layer
  cache, multi-stage builds, small/safe images (slim, distroless,
  non-root); volumes, networks, env vars and secrets; Docker Compose;
  `.dockerignore`; image scanning
- Lab: Dockerfiles for frontend and backend, `compose.yaml` with
  PostgreSQL + Redis + worker; shrink the image size
- Deliverable: `docker compose up` brings up the whole "Slot" locally +
  image size before/after

## Module 9 — Kubernetes: Orchestrating Containers
- Objectives: understand how Kubernetes works and decide honestly whether
  a project needs it
- Key concepts: the problem (many containers on many machines); cluster
  architecture (control plane: API server, etcd, scheduler, controller
  manager; nodes: kubelet, kube-proxy, container runtime); desired state
  and reconciliation; Pod, Deployment, ReplicaSet, Service, Ingress /
  Gateway API, ConfigMap, Secret, PersistentVolume, Job/CronJob; probes,
  resource limits, HPA; Helm, Kustomize; managed k8s; alternatives:
  Compose on a VPS, Docker Swarm, Nomad, PaaS; when k8s is overkill
- Lab: run "Slot" in a local cluster (k3d/minikube): manifests, Service,
  Ingress, rolling update, kill a pod and watch self-healing
- Deliverable: manifests (or a Helm chart) + a short ADR "does Slot need
  k8s?"

## Module 10 — Security: Before the App Goes Public
- Objectives: threat-model the app, fix the most common web
  vulnerabilities, and make security checks part of CI
- Key concepts: assets, entry points, attackers, STRIDE; OWASP Top 10
  (2025 edition); IDOR and per-object access checks; SQL injection and
  parameterized queries; XSS, escaping and CSP; CSRF, `SameSite` cookies,
  what CORS does and doesn't do; argon2id, login limits, MFA, sessions,
  password reset; misconfiguration; security headers; business-logic abuse
  (bots booking every slot); supply chain, lockfiles, scanning, SBOM,
  slopsquatting; personal data minimization and masking; security logging
  and fail-closed errors; gitleaks, Semgrep, pip-audit/npm audit, Trivy,
  OWASP ZAP; security review of agent-written code
- Lab: a one-page threat model; attack your own staging in pairs (IDOR,
  SQLi, XSS, brute force, mass booking); ZAP baseline; fix findings; add
  security checks to CI
- Deliverable: threat model + attack log with fixes + ZAP before/after +
  CI pipeline with security checks

## Module 11 — Infrastructure for Your First Project
- Objectives: put "Slot" on the internet on your own domain, securely and
  reproducibly
- Key concepts: hosting options: shared, VPS, PaaS (Vercel, Render,
  Fly.io, Railway), IaaS cloud (AWS, GCP, Azure, Yandex Cloud, Selectel),
  serverless; VPS basics: SSH keys, users, firewall, updates; domains and
  DNS (registrar, NS, A/AAAA, CNAME, MX, TXT, TTL); TLS (Let's Encrypt);
  reverse proxy (Nginx, Caddy, Traefik); cloud building blocks: VPC,
  managed DB, object storage (S3), CDN, load balancer; CI/CD (GitHub
  Actions → registry → deploy); secrets; backups; logs, metrics, uptime
  alerts; cost control; infrastructure as code (Terraform/OpenTofu,
  Ansible) overview
- Lab: rent a VPS, point a domain at it, deploy "Slot" with Compose behind
  Caddy with HTTPS, set up CI deploy on push, a nightly DB backup and an
  uptime check
- Deliverable: live HTTPS URL + CI pipeline + proof of a restore from
  backup

## Module 12 — Launch & Growth: Getting Your First Users
- Objectives: understand how people find apps and plan a first launch
- Key concepts: how a search engine works (crawl → index → rank);
  technical SEO (SSR/SSG, `robots.txt`, `sitemap.xml`, meta, Open Graph,
  structured data, Core Web Vitals); Google vs. Yandex specifics;
  webmaster tools; content and keywords; how social media feeds rank
  (engagement signals, watch time, early velocity, interest graph vs.
  social graph); channel choice (Telegram, VK, YouTube Shorts, TikTok,
  Habr, VC.ru, Product Hunt, Reddit); landing page, positioning, AARRR
  funnel; analytics (Yandex Metrica, GA4, UTM tags, events); privacy and
  consent basics
- Lab: make "Slot" indexable (sitemap, meta, OG, structured data), submit
  to webmaster tools, set up analytics with goals, write a launch plan for
  two channels
- Deliverable: passed SEO checklist + analytics dashboard + launch plan

## Module 13 — Capstone: Ship It
- Objectives: combine everything on one product and defend the
  architecture choices
- Key concepts: architecture review, trade-offs, what changes at 10× users
- Lab: finish "Slot" (or an own idea of similar size): docs → frontend →
  backend → containers → deploy → launch; run the launch and collect a
  week of real analytics
- Deliverable: repo + live URL + architecture diagram + ADRs + launch
  report; 10-minute demo and defense
