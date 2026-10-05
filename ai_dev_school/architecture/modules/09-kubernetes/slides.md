---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 9
## Kubernetes: Orchestrating Containers
### How a cluster works, which objects make up an app, and when you don't need k8s

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- The problem: many containers on many machines
- The core idea: desired state
- Cluster architecture
- Workloads: Pod, Deployment and friends
- Networking: Service, Ingress
- Config and storage
- Reliability: probes, limits, autoscaling
- Helm, Kustomize, GitOps
- Where to run it and when you don't need it
- Lab

---

<!-- Slide 3 -->
## Learning objectives

- Understand the problem Kubernetes solves
- Know what a cluster is made of and what each part does
- Read and write basic manifests for a web app
- Decide honestly whether a project needs Kubernetes

---

<!-- Slide 4 -->
## The problem: Docker on one machine is easy

What if there are 10 servers and 200 containers?

- Which server gets the new container?
- A server died — who restarts its containers elsewhere?
- How do you upgrade without downtime?
- How do services find each other when IPs keep changing?
- How do you scale up under load and back down?

An **orchestrator** does all of this automatically. Kubernetes (k8s) is the de facto standard.

---

<!-- Slide 5 -->
## The core idea: desired state

- You don't say "start a container". You say: **"3 copies of API version 1.4 must be running"**
- Kubernetes constantly compares the **desired** state to the **actual** one and removes the difference
- A pod died → actual 2, desired 3 → a new one is created
- This is the **reconciliation loop**

```
observe → compare with desired → act → observe → …
```

Declarative, like SQL: describe **what**, not **how**.

---

<!-- Slide 6 -->
## Cluster architecture

**Control plane** (the brain):
- **API server** — the single entry point: every command and component talks only through it
- **etcd** — a distributed key-value store: all cluster state
- **Scheduler** — decides which node a pod goes to
- **Controller manager** — runs the controllers that bring reality to the desired state

**Nodes** (the muscle):
- **kubelet** — the node agent: runs pods, reports health
- **kube-proxy** — network rules for Services
- **Container runtime** — containerd, actually runs the containers

---

<!-- Slide 7 -->
## What happens on `kubectl apply`

1. `kubectl` sends the manifest to the **API server**
2. The API server validates it and stores it in **etcd**
3. The **Deployment controller** sees: 3 pods needed, 0 exist → creates 3 Pod objects
4. The **scheduler** sees pods without a node → assigns each one a node
5. The **kubelet** on that node sees the assigned pod → asks containerd to start the container
6. The kubelet reports status → API server → etcd

Nobody calls anybody directly — everyone watches the state in the API server.

---

<!-- Slide 8 -->
## Workloads

| Object | What it is | When |
|---|---|---|
| **Pod** | One or more containers sharing a network | The smallest unit; rarely created by hand |
| **ReplicaSet** | Keeps N identical pods | Created by a Deployment |
| **Deployment** | ReplicaSet + rolling updates and rollbacks | Stateless apps: API, frontend |
| **StatefulSet** | Pods with stable names and disks | Databases, queues |
| **DaemonSet** | One pod on every node | Log collection, monitoring |
| **Job / CronJob** | A task to completion / on a schedule | Migrations, backups, reports |

---

<!-- Slide 9 -->
## Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: slot-api }
spec:
  replicas: 3
  selector: { matchLabels: { app: slot-api } }
  template:
    metadata: { labels: { app: slot-api } }
    spec:
      containers:
        - name: api
          image: ghcr.io/school/slot-api:1.4.0
          ports: [{ containerPort: 8000 }]
          envFrom: [{ secretRef: { name: slot-secrets } }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { memory: 512Mi }
          readinessProbe: { httpGet: { path: /health, port: 8000 } }
```

---

<!-- Slide 10 -->
## Networking: Service

Pods are mortal and their IPs change. A **Service** gives a stable name and address and load-balances across pods by label.

| Type | Reachable from | When |
|---|---|---|
| **ClusterIP** | Inside the cluster only | API for the frontend, DB |
| **NodePort** | A port on every node | Debugging, rarely in production |
| **LoadBalancer** | An external IP from the cloud | Public entry without Ingress |

Cluster DNS works inside: `http://slot-api.default.svc.cluster.local` or just `http://slot-api`.

---

<!-- Slide 11 -->
## Getting in from outside: Ingress and Gateway API

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: { name: slot }
spec:
  tls: [{ hosts: [slot.example], secretName: slot-tls }]
  rules:
    - host: slot.example
      http:
        paths:
          - { path: /api, pathType: Prefix, backend: { service: { name: slot-api, port: { number: 80 } } } }
          - { path: /,    pathType: Prefix, backend: { service: { name: slot-web, port: { number: 80 } } } }
```

- **Ingress** — HTTP routing rules; served by an Ingress controller (ingress-nginx, Traefik)
- **Gateway API** — the newer, more flexible successor to Ingress
- **cert-manager** issues Let's Encrypt TLS certificates automatically

---

<!-- Slide 12 -->
## Config and storage

- **ConfigMap** — non-secret settings: addresses, flags
- **Secret** — passwords, tokens. Careful: by default it's **base64, not encryption**; you need etcd encryption, RBAC, external secret managers (Vault, External Secrets)
- **PersistentVolume (PV)** — a piece of disk in the cluster
- **PersistentVolumeClaim (PVC)** — a pod's request: "I need 10 GB"; the cloud provisions a disk automatically (StorageClass)

---

<!-- Slide 13 -->
## Reliability: probes

| Probe | Question | If it fails |
|---|---|---|
| **liveness** | Is the process alive? | Restart the container |
| **readiness** | Ready to take traffic? | Remove the pod from the Service, don't kill it |
| **startup** | Has it started yet? | Hold off the other probes until it has |

A classic mistake: liveness checks the DB → the DB blips → Kubernetes restarts **every** API pod.

---

<!-- Slide 14 -->
## Reliability: resources and scaling

- **requests** — what's guaranteed; the scheduler picks a node by them
- **limits** — the ceiling; exceed memory → the container is killed (OOMKilled)
- **HPA (Horizontal Pod Autoscaler)** — changes the replica count by CPU, memory or custom metrics
- **Cluster Autoscaler** — adds and removes nodes in the cloud
- **Rolling update** — new pods come up before old ones go away; `kubectl rollout undo` — roll back

---

<!-- Slide 15 -->
## Packaging: Helm and Kustomize

- **Helm** — a package manager: manifest templates + `values.yaml`; `helm install postgresql bitnami/postgresql`
- **Kustomize** — no templates: base manifests + overlays per environment (staging, production); built into `kubectl`
- **GitOps** (Argo CD, Flux) — cluster state lives in git; a controller in the cluster syncs the cluster to git

The same desired-state principle, but the source of truth is the repo.

---

<!-- Slide 16 -->
## Where to run it

| Option | Examples | When |
|---|---|---|
| Local | k3d, kind, minikube, Docker Desktop | Learning, tests |
| A light cluster on a VPS | k3s | Small production, your own servers |
| Managed | GKE, EKS, AKS, Yandex Managed Kubernetes | The control plane is the cloud's problem |

Managed k8s removes the hardest part — the control plane, etcd, upgrades.

---

<!-- Slide 17 -->
## When you don't need Kubernetes

- One or two servers, one team, moderate load
- Nobody who will fix the cluster when it breaks at 3 a.m.
- Kubernetes adds dozens of new concepts, YAML, networking, cluster monitoring, upgrades

| Alternative | When |
|---|---|
| **Compose on one VPS** | MVPs and small projects |
| **PaaS** (Render, Fly.io, Railway) | You don't want to deal with servers at all |
| **Docker Swarm, Nomad** | Several servers, but simpler than k8s |

---

<!-- Slide 18 -->
## Kubernetes and AI agents

- Agents generate manifests and Helm charts well — and generate **dangerous** manifests just as well
- Check: probes, requests/limits, `runAsNonRoot`, no plain-text secrets, no `latest`
- Validate in CI: `kubectl apply --dry-run=server`, kubeconform, policies (Kyverno)
- Don't give an agent `kubectl` with rights on the production cluster

---

<!-- Slide 19 -->
## Lab

1. Start a local cluster: `k3d cluster create slot`
2. "Slot" manifests: Deployment + Service for the API and frontend, a StatefulSet or Helm chart for PostgreSQL, ConfigMap, Secret, Ingress
3. Do a rolling update to a new version and a rollback
4. Delete a pod — watch it come back
5. Scale the API to 5 replicas
6. **With an agent:** generate manifests from `compose.yaml` with the agent, then review by hand: probes, limits, secrets

---

<!-- Slide 20 -->
## Deliverable

- "Slot" manifests (or a Helm chart) in the repo
- A log of self-healing and the rolling update
- A list of fixes to the agent's manifests
- An ADR "does Slot need Kubernetes?" — with an honest answer

---

<!-- Slide 21 -->
## Recap and next module

- Kubernetes keeps the **desired state** through reconciliation loops
- Control plane: API server, etcd, scheduler, controllers; nodes: kubelet, kube-proxy, runtime
- Deployment + Service + Ingress are the core of a web app
- For a small project, Compose on a VPS is a fine choice
- Next: **Module 10 — Security**: looking at "Slot" through an attacker's eyes before it goes public
