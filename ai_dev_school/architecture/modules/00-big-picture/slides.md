---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 0
## The Big Picture: How a Modern Application Works
### Frontend, backend, infrastructure and the path of one request

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- The three layers of an application
- The client–server model
- The life of one request: from URL to pixels
- Protocols: HTTP, REST, WebSocket, gRPC, GraphQL
- Why each layer has its own languages
- Architecture styles: monolith, microservices, serverless
- Where AI fits in the picture
- The course project "Slot" and the lab

---

<!-- Slide 3 -->
## Learning objectives

- Explain what **frontend**, **backend** and **infrastructure** are
- Trace a request from the browser to the database and back
- Explain **why** the browser runs JavaScript while the server can run any language
- Tell a monolith from microservices and know which one to start with

---

<!-- Slide 4 -->
## The three layers of an application

| Layer | What it does | Where it runs | Analogy |
|---|---|---|---|
| **Frontend** | Shows the UI, reacts to clicks | Browser, phone | The dining room |
| **Backend** | Business logic, data, permissions | Server | The kitchen |
| **Infrastructure** | Servers, network, DB, deploy, monitoring | Data center / cloud | The building, power, plumbing |

Guests only see the dining room — but without the kitchen and the building there is no restaurant.

---

<!-- Slide 5 -->
## The client–server model

- The **client** asks: a browser, a mobile app, another service, an AI agent
- The **server** answers: checks permissions, runs logic, reads and writes data
- The client **cannot be trusted**: the server re-validates everything it receives
- Data lives on the server — the client only gets a copy to display

---

<!-- Slide 6 -->
## The life of a request: https://slot.example/booking

1. **URL** → the browser parses scheme, domain, path
2. **DNS** → the domain becomes an IP address
3. **TCP + TLS** → connection and encryption
4. **CDN** → static files come from the nearest edge node
5. **Load balancer / reverse proxy** → picks an app server
6. **API** → permission check, business logic
7. **DB / cache / queue** → data
8. **Response** → JSON or HTML back
9. **Rendering** → the browser paints pixels

---

<!-- Slide 7 -->
## Step 2: DNS — the internet's phone book

- `slot.example` → `203.0.113.10`
- The resolver walks the chain: root servers → `.example` → the domain's NS servers
- The answer is cached for its **TTL**
- That's why a DNS change doesn't apply instantly

We'll go deeper in Module 11, when we connect our own domain.

---

<!-- Slide 8 -->
## Step 3: TCP + TLS

- **TCP** — reliable byte delivery: handshake, ordering, retransmission
- **TLS** — encryption plus proof the server is who it claims to be
- The padlock in the address bar = a valid TLS certificate
- HTTP/2 and HTTP/3 (QUIC) cut down handshakes and speed up loading

---

<!-- Slide 9 -->
## Steps 4–5: CDN and reverse proxy

- **CDN** — servers around the world caching images, JS, CSS close to the user
- **Reverse proxy** (Nginx, Caddy) — one entry point: TLS, routing, compression
- **Load balancer** spreads requests across several copies of the app
- The user sees one address — there may be a dozen servers behind it

---

<!-- Slide 10 -->
## Steps 6–7: API and data

- **API** — a contract: which requests you can make and what comes back
- Inside: routing → validation → authorization → business logic → data access
- **Database** holds state (PostgreSQL, MySQL, MongoDB)
- **Cache** (Redis) — fast answers to frequent questions
- **Queue** — slow work in the background: emails, notifications, reports

---

<!-- Slide 11 -->
## HTTP in one minute

```
POST /api/bookings HTTP/1.1
Host: slot.example
Content-Type: application/json
Authorization: Bearer eyJhbGciOi...

{"slot_id": 42, "client_name": "Anna"}
```

```
HTTP/1.1 201 Created
Content-Type: application/json

{"id": 1017, "status": "confirmed"}
```

Methods: GET, POST, PUT/PATCH, DELETE · Codes: 2xx success, 3xx redirect, 4xx client error, 5xx server error

---

<!-- Slide 12 -->
## Ways for client and server to talk

| Protocol | How it works | When to use |
|---|---|---|
| **REST** | HTTP + JSON, resources and methods | Default for public APIs |
| **GraphQL** | The client describes which fields it needs | Complex frontend, lots of related data |
| **WebSocket** | A persistent two-way connection | Chats, real-time notifications |
| **gRPC** | Binary protocol, strict schema (protobuf) | Service-to-service calls |

---

<!-- Slide 13 -->
## Why the frontend is JavaScript

- The browser only runs **HTML, CSS, JavaScript** (+ **WebAssembly**)
- **TypeScript** is JavaScript with types; it compiles to plain JS
- React, Vue, Svelte — all of it ends up as JS in the browser
- WebAssembly lets the browser run Rust, C++, Go — for heavy work (Figma, video, games)
- Mobile clients: Swift (iOS), Kotlin (Android) or cross-platform — React Native, Flutter

---

<!-- Slide 14 -->
## Why the backend can be any language

The server is your machine — you can run anything on it. The choice comes down to:

| Language | Strength |
|---|---|
| Python | Development speed, the AI/ML ecosystem |
| Go | Simplicity, performance, a single binary |
| JavaScript/TypeScript | One language for front and back |
| Rust | Maximum speed and memory safety |
| Java/Kotlin, C# | Enterprise, large teams |

Details in Module 3.

---

<!-- Slide 15 -->
## Infrastructure and its languages

- **Where to run:** VPS, cloud, Kubernetes, PaaS
- **How to package:** Docker (`Dockerfile`)
- **How to describe:** configuration as code — **YAML** (Compose, Kubernetes, CI), **HCL** (Terraform), **Bash**
- **How to watch:** logs, metrics, alerts
- Principle: infrastructure is described in files in the repo, not "set up by hand at some point"

---

<!-- Slide 16 -->
## Architecture styles

| Style | Idea | Pros | Cons |
|---|---|---|---|
| **Monolith** | One app, one deploy | Simple, fast | Grows into a "big ball of mud" |
| **Modular monolith** | One deploy, clear modules inside | Simplicity + order | Needs discipline |
| **Microservices** | Many services, each deployed separately | Independent teams and scaling | Network, complexity, cost |
| **Serverless** | Functions the cloud runs for you | No servers, pay per call | Cold starts, vendor lock-in |

---

<!-- Slide 17 -->
## Why start with a monolith

- Microservices solve an **organizational** problem: many teams getting in each other's way
- A startup of 1–5 people doesn't have that problem
- Every network call between services is a new point of failure
- A good modular monolith is easy to split later; bad microservices are hard to glue back

> Monolith first. Split when it hurts, not when it's trendy.

---

<!-- Slide 18 -->
## Where AI fits in the picture

- **LLM APIs** (Claude, GPT, etc.) — one more external backend dependency, like a payment gateway
- LLM calls are slow and expensive → queues, caching, limits, timeouts
- **AI agents as clients**: they read your API and docs, call tools (MCP)
- **AI agents as developers**: they write code from your docs — that's why every lab in this course has a "With an agent" step

---

<!-- Slide 19 -->
## The course project: "Slot"

Online booking for a small business — a barber, a tutor, a meeting room.

- Public page: services and free slots (needs SEO)
- The client books a slot
- An admin panel for the owner
- Booking notifications

Every module adds one layer to "Slot" — by the end of the course it runs on your own domain.

---

<!-- Slide 20 -->
## Lab

1. Open DevTools → the **Network** tab on a real site (a marketplace, a news site)
2. Reload the page, save the trace (**HAR**)
3. Find: the HTML document, CDN static files, API calls, the slowest request
4. Draw the architecture you can infer from the outside
5. **With an agent:** give the agent the HAR file, ask it to explain every request; find where it got things wrong

---

<!-- Slide 21 -->
## Deliverable

- An annotated request trace
- An architecture diagram of the site you studied
- The first block diagram of "Slot": client → API → DB, notifications
- A list of the agent's mistakes and why it made them

---

<!-- Slide 22 -->
## Recap and next module

- Application = frontend + backend + infrastructure
- One click passes through DNS, TLS, CDN, proxy, API, DB
- The browser dictates JavaScript; the server can use any language
- Start with a monolith
- Next: **Module 1 — Project Documentation**: describing "Slot" so that a person and an agent build the same thing
