---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 13
## Capstone: Ship It
### Every layer of the course in one live product

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- The capstone goal
- Requirements map: module → artifact
- Choosing a project
- Work plan and checkpoints
- Working with agents across the whole project
- Typical failures
- The "10× users" question
- Defense and grading

---

<!-- Slide 3 -->
## Learning objectives

- Combine every layer of the course into one **live** product
- Defend architecture decisions with ADRs and numbers
- Run a real launch and analyze the results
- Explain what changes in the architecture as it grows

---

<!-- Slide 4 -->
## The product's journey: the whole course on one slide

**Idea → Docs → Frontend → Backend → API & data → Performance → AI → Containers → Security → Infrastructure → Launch**

| Module | The question you answered |
|---|---|
| 0 | What layers is an application made of? |
| 1 | What exactly are we building and how do we check it? |
| 2–3 | What do we build the front and back with, and why? |
| 4–5 | What contract does the API keep, and how does the data stay correct? |
| 6 | Is it fast enough — and how do we know? |
| 7 | How does an LLM fit in safely and affordably? |
| 8–9 | How do we package it and run it the same everywhere? |
| 10 | Is it safe to put online? |
| 11 | How does it run reliably on the internet? |
| 12 | How will people find out about it? |

---

<!-- Slide 5 -->
## Requirements map

| Layer | Minimum to pass |
|---|---|
| **Docs** | Vision, user stories with criteria, BPMN of the main process, C4 Container, OpenAPI, ADRs, `AGENTS.md` |
| **Frontend** | A public SEO page + an interactive part; an ADR on the framework |
| **Backend** | An API with auth, tests, one background job |
| **API & data** | One error format, pagination, idempotent booking; DB constraints against double booking; a zero-downtime migration |
| **Performance** | A load test with p95 and RPS; one bottleneck found and fixed |
| **AI** | One LLM feature with timeouts, limits, a cost estimate and an eval set |
| **Containers** | `docker compose up` starts everything; k8s manifests optional |
| **Security** | A threat model, the OWASP checklist, dependency and image scanning in CI |
| **Infrastructure** | Own domain, HTTPS, CI deploy, a tested backup, monitoring |
| **Launch** | SEO basics, analytics with goals, a launch in at least one channel, a week of data |

---

<!-- Slide 6 -->
## Choosing a project

- **Default:** "Slot" — much of it is already built in the labs
- **Your own idea** — allowed if it's similar in size and approved by the instructor
- A good own idea: has a public page, data, a process, and a real audience you know
- A bad own idea: "a social network for everyone", "a marketplace", anything you can't demo in 10 minutes

> A small but live product beats a big but unfinished one.

---

<!-- Slide 7 -->
## Work plan

| Week | Focus | Checkpoint |
|---|---|---|
| 1 | Docs, data model, frontend and backend skeletons | `docs/` agreed, the API responds |
| 2 | Features, API contract, tests, the AI feature | The main scenario works end to end |
| 3 | Containers, security pass, deploy, monitoring | A live HTTPS address, CI is green |
| 4 | Performance, SEO, analytics, launch | A week of real data, the report |

Each checkpoint is a short demo to the instructor. Problems surface early.

---

<!-- Slide 8 -->
## Working with agents across the whole project

- `AGENTS.md` from day one; update it with every architecture decision
- The agent works **from the docs**: user story → test → code
- Every agent change goes through review and CI, like a human's
- The agent gets only test secrets and staging; production is your hands
- Keep an **agent log**: what you delegated, what came out, what you had to fix

The log is part of the defense: it shows you directed the agent, not the other way around.

---

<!-- Slide 9 -->
## Typical failures

| Failure | How to avoid it |
|---|---|
| Beautiful architecture, nothing works | Main scenario end to end first, the rest later |
| Deploying on the last night | A live address by the end of week 3 |
| Docs drift from the code | Update them in the same PR as the code |
| Microservices and Kubernetes "because it's trendy" | Monolith + Compose unless there's a reason |
| Launch without analytics | Goals set up before the first post |
| The backup was never tested | A restore is part of passing |

---

<!-- Slide 10 -->
## The "10× users" question

At the defense you'll be asked: **what changes if there are 10 times more users?**

A good answer relies on numbers and names the **first** bottleneck:

- "The load test showed a limit of ~400 RPS on one VPS; we'll hit the API's CPU first → a second copy behind a load balancer, sessions are already in Redis"
- "The DB is next: move it to managed PostgreSQL with a read replica"
- "Kubernetes isn't needed yet: Compose handles two servers fine"

A bad answer: "we'll rewrite it as microservices in Rust".

---

<!-- Slide 11 -->
## Defense: 10 minutes

1. **Live demo** on the production address — the main scenario end to end (3 min)
2. **Architecture:** C4 Container and the three most important ADRs (2 min)
3. **What broke** during the course and how you fixed it (2 min)
4. **Launch results:** visitors, conversions, what you'd change (2 min)
5. **"10× users?"** (1 min) + questions

---

<!-- Slide 12 -->
## Grading

| Criterion | Weight |
|---|---|
| The product runs in production, the main scenario has no errors | 25% |
| Docs are complete and match the code | 15% |
| Architecture decisions are justified (ADRs, numbers) | 15% |
| Code, API contract, data integrity and tests | 15% |
| Infrastructure and security: CI, HTTPS, backup, monitoring, OWASP checklist | 15% |
| Launch: analytics, a channel, an honest analysis of results | 15% |

Bonus: Kubernetes manifests, a second backend language, a strong AI eval set, an interesting agent log.

---

<!-- Slide 13 -->
## Deliverable

- The repository: code, `docs/`, `AGENTS.md`, Dockerfile, `compose.yaml`, CI
- A live product address
- An architecture diagram and ADRs
- A launch report: channels, funnel numbers, conclusions
- The agent log

---

<!-- Slide 14 -->
## What's next

- Keep developing the product: you have real users and metrics
- The **"Agentic Software Development"** course — directing agents on complex tasks
- Going deeper: Kubernetes in production, observability, system design for high-load systems
- Publish: a Habr article about your launch is a promotion channel too

---

<!-- Slide 15 -->
## Course recap

- Application = frontend + backend + infrastructure + the people who found out about it
- Documentation is a contract for people and agents
- Choose technologies with arguments and numbers, not fashion
- A simple solution that works beats a complex one "for future growth"
- Measure everything: speed, reliability, the funnel
