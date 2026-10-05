# Module 13 — Capstone: Ship It

## Learning objectives
- Combine every layer of the course into one live product
- Defend architecture choices with ADRs and numbers
- Run a real launch and read its results

## Requirements
1. **Docs:** vision, user stories with acceptance criteria, BPMN of the main flow, C4 container diagram, OpenAPI, ADRs (Module 1)
2. **Frontend:** public SEO page + interactive part; framework choice justified (Module 2)
3. **Backend:** API with auth, tests, one background job (Module 3)
4. **API design:** consistent errors, pagination, idempotent booking, versioning; the OpenAPI matches the code (Module 4)
5. **Data:** constraints that make double booking impossible, migrations, at least one zero-downtime migration (Module 5)
6. **Performance:** a load test with p95 and RPS, one bottleneck found and fixed (Module 6)
7. **AI feature:** one LLM feature with timeouts, limits, a cost estimate and an eval set (Module 7)
8. **Containers:** everything starts with `docker compose up` (Module 8); k8s manifests optional (Module 9)
9. **Security:** threat model, OWASP checklist passed, dependency and image scanning in CI (Module 10)
10. **Infrastructure:** own domain, HTTPS, CI deploy, backups, uptime monitoring (Module 11)
11. **Launch:** SEO basics, analytics with goals, launch in at least one channel, a week of data (Module 12)

## Project
"Slot" from the course, or an own idea of similar size approved by the instructor.

## Defense (10 minutes)
- Live demo on the production URL
- Architecture diagram and the three most important ADRs
- What broke during the course and how you fixed it
- Launch results: visitors, conversions, what you'd change
- "What changes at 10× users?"

## Deliverable
Repository + live URL + architecture diagram + ADRs + launch report.
