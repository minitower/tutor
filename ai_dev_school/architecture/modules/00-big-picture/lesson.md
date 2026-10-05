# Module 0 — The Big Picture: How a Modern Application Works

## Learning objectives
- Explain what frontend, backend and infrastructure are and how they talk to each other
- Explain why each layer uses the languages it does
- Trace one request from the browser to the database and back

## Lecture outline
1. Client–server model: who asks, who answers, where the data lives
2. The life of a request: URL → DNS → TCP/TLS → CDN → load balancer / reverse proxy → API → database → response → rendering
3. Protocols and formats: HTTP methods and status codes, REST, JSON, WebSocket, gRPC, GraphQL (overview)
4. Frontend: the browser runs only HTML/CSS/JS (+ WebAssembly); why TypeScript compiles to JS; mobile and desktop clients
5. Backend: the server can run any language; what decides the choice (ecosystem, speed, team, hiring)
6. Infrastructure: servers, networks, databases, queues, CDN; config and IaC languages (YAML, HCL, Bash)
7. Architecture styles: monolith, modular monolith, microservices, serverless; why most projects should start as a monolith
8. Where AI fits: LLM APIs as one more backend dependency; agents as a new kind of client

## Lab
Open DevTools on a real site (e.g. a marketplace or a news site). Trace one page load: DNS time, the HTML document, static assets, API calls, timings. Draw the architecture you can infer from the outside.
- **With an agent:** give the agent your trace (HAR file) and ask it to explain each request; check where it guessed wrong.

## Deliverable
Annotated request trace + the first block diagram of "Slot" (client, API, DB, notifications).
