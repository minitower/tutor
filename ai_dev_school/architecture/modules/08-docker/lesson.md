# Module 8 — Docker: Packaging the Application

## Learning objectives
- Understand what a container is under the hood and how it differs from a VM
- Write a good Dockerfile and a Compose file for a multi-service app
- Know why containers became the standard unit of deployment

## Lecture outline
1. The problem: "works on my machine", dependency conflicts, environment drift
2. VM vs. container: hypervisor + full OS vs. shared kernel + isolated process
3. Under the hood: Linux namespaces (isolation), cgroups (limits), layered filesystem (OverlayFS)
4. Core terms: image, layer, container, registry (Docker Hub, GHCR), tag vs. digest
5. Docker architecture: CLI → Docker Engine (daemon) → containerd → runc; OCI standard; Podman as an alternative
6. Dockerfile: `FROM`, `RUN`, `COPY`, `CMD`/`ENTRYPOINT`; layer cache and instruction order; `.dockerignore`
7. Multi-stage builds; small and safe images: slim, alpine, distroless, non-root user, no secrets in layers
8. Runtime: ports, volumes vs. bind mounts, networks, env vars, healthchecks, restart policies
9. Docker Compose: a whole app in one file; service dependencies, local dev vs. production
10. Security basics: image scanning (Trivy, Docker Scout), pinning versions

## Lab
Write Dockerfiles for the "Slot" frontend and backend and a `compose.yaml` with PostgreSQL, Redis and a worker. Shrink the backend image with a multi-stage build.
- **With an agent:** ask the agent to review your Dockerfile for cache order, image size and security; check every suggestion by rebuilding.

## Deliverable
`docker compose up` brings up the whole "Slot" locally + image size before/after.
