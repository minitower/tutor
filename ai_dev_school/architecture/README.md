# Modern Application Architecture: From Idea to a Live Product

A course about how a modern web application is actually built and run:
what lives on the frontend, the backend and in the infrastructure, which
languages and frameworks fit each layer and why, how the app gets packed
into containers and run in the cloud, how it is documented so that both
people and AI agents can work with it, and how it finds its first users.

The course is built around **one running project** (see below): each
module adds one layer to it, so by the end students have a documented,
containerized app deployed on their own domain.

## Who this is for

Students who already write code in at least one language (Python is
enough) and have built small scripts or bots, but have never seen how a
full product fits together. It does not re-teach programming basics.
Pairs well with [ai-agent-dev-course](../ai-agent-dev-course/): here
students learn *what* to build, there they learn *how to direct an agent*
that builds it.

## Format (assumed — adjust to taste)

- 14 modules (00–13), ~2–3 hours each (lecture + lab)
- Every lab extends the same running project
- Every lab has a "with an agent" step: students give an AI coding agent
  the module's artifacts (docs, Dockerfile, configs) and check its output
- Capstone in the final module: the project goes live and gets its first
  real visitors

## Running project

**"Slot" — an online booking service for a small business** (a barber,
a tutor, a coworking room): a public page with services and free slots,
booking by the client, an admin panel for the owner, notifications.
Small enough to finish, but touches every topic: user stories and BPMN for
the booking flow, a public SEO page + an admin SPA on the frontend, an API
with a database and background jobs on the backend, containers, a domain
with TLS, and a real audience to promote to.

## Learning outcomes

By the end, a student can:
1. Draw the path of a request from a browser to the database and back,
   and name what runs at each step and why it is written in that language
2. Describe a product with user stories, use cases, test cases, BPMN and
   UML/C4 diagrams in a form an AI agent can read and implement against
3. Choose a frontend approach (SPA / SSR / SSG) and framework for a task
   and justify the choice
4. Choose a backend language and framework for a task, and find and fix
   the real performance bottleneck instead of guessing
5. Design an API that survives retries, concurrent edits and version
   changes, and a database schema that enforces the business rules itself
6. Build an LLM feature into a backend — streaming, structured outputs,
   tools, RAG — with limits, evals and defenses against prompt injection
7. Package an app with Docker and Compose, and explain when Kubernetes is
   (and is not) worth it
8. Threat-model an app, fix the OWASP Top 10 classics and put security
   checks into CI
9. Deploy the app to a VPS or a cloud with a domain, DNS, TLS, CI/CD,
   backups and basic monitoring
10. Make the app findable: SEO basics, how recommendation feeds work,
    launch channels and analytics

## Structure

See [syllabus.md](syllabus.md) for the full outline. Per-module detail
lives in [modules/](modules/). Each module folder has the lesson
(`lesson.md` / `lesson.ru.md`), Marp slide sources (`slides.md` /
`slides.ru.md`) and an interactive Russian deck (`slides.html`, styled by
[assets/](assets/) — open it through a local server, not as a file).
Lecture scripts come next, in the same format as the main course.

| # | Module | Focus | Lesson | Slides |
|---|--------|-------|--------|--------|
| 0 | The Big Picture | Frontend / backend / infrastructure, request lifecycle | [EN](modules/00-big-picture/lesson.md) · [RU](modules/00-big-picture/lesson.ru.md) | [EN](modules/00-big-picture/slides.md) · [RU](modules/00-big-picture/slides.ru.md) · [HTML](modules/00-big-picture/slides.html) |
| 1 | Project Documentation | User story, use case, test case, BPMN, UML/C4, docs for agents | [EN](modules/01-project-documentation/lesson.md) · [RU](modules/01-project-documentation/lesson.ru.md) | [EN](modules/01-project-documentation/slides.md) · [RU](modules/01-project-documentation/slides.ru.md) · [HTML](modules/01-project-documentation/slides.html) |
| 2 | Frontend Frameworks | React, Vue, Angular, Svelte, Next/Nuxt/Astro; SPA vs SSR vs SSG | [EN](modules/02-frontend-frameworks/lesson.md) · [RU](modules/02-frontend-frameworks/lesson.ru.md) | [EN](modules/02-frontend-frameworks/slides.md) · [RU](modules/02-frontend-frameworks/slides.ru.md) · [HTML](modules/02-frontend-frameworks/slides.html) |
| 3 | Backend Languages & Frameworks | Python, Go, Node/TS, Rust, Java/C#; FastAPI, Django, Gin, Axum… | [EN](modules/03-backend-frameworks/lesson.md) · [RU](modules/03-backend-frameworks/lesson.ru.md) | [EN](modules/03-backend-frameworks/slides.md) · [RU](modules/03-backend-frameworks/slides.ru.md) · [HTML](modules/03-backend-frameworks/slides.html) |
| 4 | API Design | Errors, pagination, idempotency, ETag, versioning, webhooks, contract-first | [EN](modules/04-api-design/lesson.md) · [RU](modules/04-api-design/lesson.ru.md) | [EN](modules/04-api-design/slides.md) · [RU](modules/04-api-design/slides.ru.md) · [HTML](modules/04-api-design/slides.html) |
| 5 | Databases | Modeling, constraints, transactions, isolation, zero-downtime migrations, scaling | [EN](modules/05-databases/lesson.md) · [RU](modules/05-databases/lesson.ru.md) | [EN](modules/05-databases/slides.md) · [RU](modules/05-databases/slides.ru.md) · [HTML](modules/05-databases/slides.html) |
| 6 | Backend Performance | Percentiles, profiling, indexes, caching, queues, load testing | [EN](modules/06-backend-performance/lesson.md) · [RU](modules/06-backend-performance/lesson.ru.md) | [EN](modules/06-backend-performance/slides.md) · [RU](modules/06-backend-performance/slides.ru.md) · [HTML](modules/06-backend-performance/slides.html) |
| 7 | AI Inside the App | LLM calls, streaming, structured outputs, tools, RAG, evals, cost, injection | [EN](modules/07-ai-in-the-app/lesson.md) · [RU](modules/07-ai-in-the-app/lesson.ru.md) | [EN](modules/07-ai-in-the-app/slides.md) · [RU](modules/07-ai-in-the-app/slides.ru.md) · [HTML](modules/07-ai-in-the-app/slides.html) |
| 8 | Docker | Containers, images, Dockerfile, Compose | [EN](modules/08-docker/lesson.md) · [RU](modules/08-docker/lesson.ru.md) | [EN](modules/08-docker/slides.md) · [RU](modules/08-docker/slides.ru.md) · [HTML](modules/08-docker/slides.html) |
| 9 | Kubernetes | Cluster architecture, objects, Helm, when you need it | [EN](modules/09-kubernetes/lesson.md) · [RU](modules/09-kubernetes/lesson.ru.md) | [EN](modules/09-kubernetes/slides.md) · [RU](modules/09-kubernetes/slides.ru.md) · [HTML](modules/09-kubernetes/slides.html) |
| 10 | Security | Threat modeling, OWASP Top 10, auth, headers, supply chain, CI checks | [EN](modules/10-security/lesson.md) · [RU](modules/10-security/lesson.ru.md) | [EN](modules/10-security/slides.md) · [RU](modules/10-security/slides.ru.md) · [HTML](modules/10-security/slides.html) |
| 11 | Infrastructure for Your First Project | VPS, DNS, TLS, cloud services, CI/CD, monitoring | [EN](modules/11-infrastructure/lesson.md) · [RU](modules/11-infrastructure/lesson.ru.md) | [EN](modules/11-infrastructure/slides.md) · [RU](modules/11-infrastructure/slides.ru.md) · [HTML](modules/11-infrastructure/slides.html) |
| 12 | Launch & Growth | Search engines, SEO, social media algorithms, analytics | [EN](modules/12-launch-and-growth/lesson.md) · [RU](modules/12-launch-and-growth/lesson.ru.md) | [EN](modules/12-launch-and-growth/slides.md) · [RU](modules/12-launch-and-growth/slides.ru.md) · [HTML](modules/12-launch-and-growth/slides.html) |
| 13 | Capstone | Ship "Slot" end to end and get first users | [EN](modules/13-capstone/lesson.md) · [RU](modules/13-capstone/lesson.ru.md) | [EN](modules/13-capstone/slides.md) · [RU](modules/13-capstone/slides.ru.md) · [HTML](modules/13-capstone/slides.html) |

## Why this order

Docs come right after the big picture, because the spec is what every
later module (and every agent) builds against. API design and databases
follow the backend frameworks, because they are the contract and the data
the backend is built around; performance comes after them, because most
bottlenecks live in exactly those two places. The AI module comes once
students know queues, caching and timeouts, because an LLM is the slowest
and most expensive dependency of all. Docker and Kubernetes come after the
app exists, security comes right before the app goes public, and
infrastructure comes after containers, because a container is the thing
you deploy. Promotion comes last, once there is a live URL to promote.

## Open questions to settle before running this course

- Cloud provider for labs: a Russian provider (Yandex Cloud, Selectel,
  Timeweb Cloud) vs. a global one (AWS, GCP, Hetzner, DigitalOcean).
  This affects payment, free tiers and the DNS/registrar walkthrough
- Who pays for the VPS and domain in Module 11 (school or student)?
- Fixed stack for the running project (e.g. FastAPI + Next.js +
  PostgreSQL) vs. each student picks after Modules 2–3
- Is Kubernetes a hands-on lab (k3d/minikube locally) or a demo only?
