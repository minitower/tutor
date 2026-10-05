# Module 9 — Kubernetes: Orchestrating Containers

## Learning objectives
- Understand the problem Kubernetes solves and how a cluster is built
- Read and write basic manifests for a web application
- Decide honestly whether a project needs Kubernetes

## Lecture outline
1. The problem: many containers on many machines; restarts, scaling, rolling updates, service discovery
2. Core idea: declarative desired state + controllers that reconcile reality to it
3. Cluster architecture
   - Control plane: API server, etcd, scheduler, controller manager
   - Nodes: kubelet, kube-proxy, container runtime (containerd)
4. Workloads: Pod, ReplicaSet, Deployment, StatefulSet, DaemonSet, Job/CronJob
5. Networking: Service (ClusterIP, NodePort, LoadBalancer), Ingress, Gateway API, DNS inside the cluster
6. Config and storage: ConfigMap, Secret, PersistentVolume / PersistentVolumeClaim
7. Reliability: liveness/readiness probes, resource requests and limits, HPA, rolling updates and rollbacks
8. Packaging: Helm and Kustomize; GitOps (Argo CD, Flux) overview
9. Where to run: local (k3d, kind, minikube), managed (GKE, EKS, AKS, Yandex Managed Kubernetes), k3s on a VPS
10. When you don't need it: Compose on one VPS, Docker Swarm, Nomad, PaaS; the operational cost of k8s

## Lab
Run "Slot" in a local cluster (k3d or minikube): Deployments, Services, Ingress, ConfigMap/Secret. Do a rolling update, kill a pod and watch self-healing, scale the API.
- **With an agent:** generate manifests from `compose.yaml` with the agent, then review them by hand: probes, limits, secrets.

## Deliverable
Manifests (or a Helm chart) + a short ADR "does Slot need Kubernetes?".
