---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 8
## Docker: Packaging the Application
### What a container is under the hood, and how to package "Slot" so it runs the same everywhere

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- The "works on my machine" problem
- Virtual machine vs container
- Under the hood: namespaces, cgroups, layers
- Image, container, registry
- Docker architecture
- Dockerfile, layer cache, multi-stage
- Volumes, networks, environment variables
- Docker Compose
- Image security
- Lab: all of "Slot" with one command

---

<!-- Slide 3 -->
## Learning objectives

- Understand what a container is and how it differs from a virtual machine
- Write a Dockerfile that builds fast and produces a small, safe image
- Describe a multi-service app in Compose
- Understand why the container became the standard unit of delivery

---

<!-- Slide 4 -->
## The problem: "works on my machine"

- The developer has Python 3.12, the server has 3.9
- A library needs a system dependency (`libpq`) the server doesn't have
- Two projects on one server need different versions of the same package
- A new hire spends two days setting up their environment

A **container** packages the app **together with its environment**: interpreter, libraries, system packages, configs.

---

<!-- Slide 5 -->
## Virtual machine vs container

| | Virtual machine | Container |
|---|---|---|
| What it isolates | A whole computer with its own OS | Process(es) on a shared kernel |
| Size | Gigabytes | Tens to hundreds of megabytes |
| Startup | Minutes | Seconds or less |
| Isolation | Strong (hypervisor) | Good, but the kernel is shared |
| Density | Dozens per server | Hundreds per server |

A container is **not a small VM** — it's an ordinary Linux process with a restricted view and limited resources.

---

<!-- Slide 6 -->
## Under the hood: three Linux mechanisms

- **Namespaces** — what the process **sees**: its own PIDs, network, filesystem, hostname, users
- **cgroups** — how much the process **can take**: CPU, memory, disk, number of processes
- **Layered filesystem (OverlayFS)** — an image of read-only layers + a thin writable layer on top

On Windows and macOS, Docker Desktop runs a lightweight Linux VM, and the containers live inside it.

---

<!-- Slide 7 -->
## Image, container, registry

- **Image** — a read-only template: files + metadata (what to run, which ports)
- **Container** — a running instance of an image with its own writable layer
- **Registry** — image storage: Docker Hub, GitHub Container Registry, a cloud registry
- **Tag** — a human-readable version name (`slot-api:1.4.0`, `latest`); **digest** (`sha256:…`) — an exact, immutable fingerprint

Analogy: an image is a class, a container is an object.

---

<!-- Slide 8 -->
## Docker architecture

```
docker CLI  →  Docker Engine (dockerd)  →  containerd  →  runc  →  process
   your           daemon: API, builds,      manages          creates namespaces
   command        networks, volumes         containers       and cgroups
```

- **OCI** — an open standard for images and runtimes: an image built by Docker runs in Podman or Kubernetes
- **Podman** — a daemonless, command-compatible alternative
- Kubernetes talks to containerd directly, without Docker Engine

---

<!-- Slide 9 -->
## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Each instruction (`FROM`, `RUN`, `COPY`) creates a layer.

---

<!-- Slide 10 -->
## Layer cache and instruction order

```dockerfile
# Bad: any code change → reinstall all dependencies
COPY . .
RUN pip install -r requirements.txt

# Good: dependencies change rarely — their layer comes from cache
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Rule: **rarely changing things go higher, frequently changing things go lower**. Plus `.dockerignore`: `.git`, `node_modules`, `.venv`, `.env`.

---

<!-- Slide 11 -->
## Multi-stage builds

```dockerfile
# Stage 1: build — with all the tools
FROM node:22 AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: run — only the result
FROM nginx:alpine
COPY --from=build /src/dist /usr/share/nginx/html
```

The final frontend image: ~1.2 GB → ~50 MB. No compilers or sources in production.

---

<!-- Slide 12 -->
## Small and safe images

| Base image | Size | When |
|---|---|---|
| `python:3.12` | ~1 GB | Almost never for production |
| `python:3.12-slim` | ~130 MB | The default |
| `alpine` | ~5 MB base | Careful: musl instead of glibc, surprises with Python wheels |
| `distroless` | Minimal | Not even a shell — smaller attack surface |

Plus: run **as non-root** (`USER app`), **no secrets in layers**, pinned versions.

---

<!-- Slide 13 -->
## Running: ports, volumes, variables

```bash
docker run -d --name slot-api \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -v slot-uploads:/app/uploads \
  --restart unless-stopped \
  --memory 512m --cpus 1 \
  slot-api:1.4.0
```

- `-p` host port : container port · `-e` config via environment · `-v` named volume · `--memory/--cpus` limits (cgroups)
- A container is **disposable**: anything written inside without a volume is lost on re-creation
- **Volumes** — data that outlives the container; **bind mount** — a host folder (for development)

---

<!-- Slide 14 -->
## Networks and healthchecks

- Containers in one user-defined network see each other **by service name**: `postgres:5432`
- Publish only what's needed (`-p`); never expose the DB to the outside
- A **healthcheck** is a command that checks the app is actually alive, not just started

```dockerfile
HEALTHCHECK --interval=10s CMD curl -f http://localhost:8000/health || exit 1
```

---

<!-- Slide 15 -->
## Docker Compose: the whole app in one file

```yaml
services:
  api:
    build: ./api
    environment:
      DATABASE_URL: postgresql://slot:${DB_PASSWORD}@postgres:5432/slot
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres: { condition: service_healthy }
    ports: ["8000:8000"]
  worker:
    build: ./api
    command: arq app.worker.Settings
  postgres:
    image: postgres:17
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD", "pg_isready", "-U", "slot"] }
  redis:
    image: redis:7
volumes:
  pgdata:
```

---

<!-- Slide 16 -->
## Compose: development and production

- `docker compose up` — start everything; `down` — stop; `logs -f api` — follow logs
- **Development:** bind-mounted code + auto-reload; `compose.override.yaml` is picked up automatically
- **Production:** only prebuilt images from a registry, secrets from the environment, `restart: unless-stopped`
- Compose on one VPS is an honest production option for a small project (Module 11)

---

<!-- Slide 17 -->
## Image security

- **Vulnerability scanning:** Trivy, Docker Scout, Grype — in CI on every build
- **Pinned versions:** `postgres:17.2`, not `latest`; for maximum precision — a digest
- **Non-root** inside the container
- **Secrets** via environment variables or secrets, never in the `Dockerfile` or layers
- **Minimal image** — fewer packages, fewer vulnerabilities

---

<!-- Slide 18 -->
## Docker and AI agents

- A container is a **sandbox** for an agent: it runs code and tests without touching your system
- Agents write Dockerfiles well, but often: copy everything before installing deps, forget `.dockerignore`, leave root
- The check is simple: rebuild after changing one line of code and see how many layers came from the cache

---

<!-- Slide 19 -->
## Lab

1. A Dockerfile for the "Slot" backend (FastAPI) and frontend (multi-stage)
2. `compose.yaml`: api, worker, PostgreSQL, Redis, frontend
3. Healthchecks, a volume for the DB, non-root user, `.dockerignore`
4. Shrink the backend image: record the size before and after
5. Scan the image with Trivy
6. **With an agent:** ask the agent to review the Dockerfile for cache order, size and security; verify each suggestion by rebuilding

---

<!-- Slide 20 -->
## Deliverable

- `docker compose up` brings up all of "Slot" locally
- Image sizes before/after and what made the difference
- The Trivy report and what you fixed
- Which of the agent's suggestions a rebuild confirmed, and which it didn't

---

<!-- Slide 21 -->
## Recap and next module

- Container = process + namespaces + cgroups + layers
- An image is a template, a container a running instance, a registry the warehouse
- Instruction order decides the cache; multi-stage decides the size
- Compose describes the whole app in one file
- Next: **Module 9 — Kubernetes**: what to do when there are many containers and servers
