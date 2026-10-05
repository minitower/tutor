# Модуль 9 — Kubernetes: оркестрация контейнеров

## Цели обучения
- Понимать, какую проблему решает Kubernetes и как устроен кластер
- Читать и писать базовые манифесты для веб-приложения
- Честно решать, нужен ли проекту Kubernetes

## План лекции
1. Проблема: много контейнеров на многих машинах; перезапуски, масштабирование, плавные обновления, обнаружение сервисов
2. Основная идея: декларативное желаемое состояние + контроллеры, которые приводят реальность к нему
3. Архитектура кластера
   - Control plane: API server, etcd, scheduler, controller manager
   - Узлы: kubelet, kube-proxy, container runtime (containerd)
4. Рабочие нагрузки: Pod, ReplicaSet, Deployment, StatefulSet, DaemonSet, Job/CronJob
5. Сеть: Service (ClusterIP, NodePort, LoadBalancer), Ingress, Gateway API, DNS внутри кластера
6. Конфигурация и хранилище: ConfigMap, Secret, PersistentVolume / PersistentVolumeClaim
7. Надёжность: liveness/readiness-пробы, requests и limits ресурсов, HPA, rolling update и откат
8. Упаковка: Helm и Kustomize; обзор GitOps (Argo CD, Flux)
9. Где запускать: локально (k3d, kind, minikube), managed (GKE, EKS, AKS, Yandex Managed Kubernetes), k3s на VPS
10. Когда он не нужен: Compose на одном VPS, Docker Swarm, Nomad, PaaS; операционная стоимость k8s

## Лабораторная работа
Запустите «Slot» в локальном кластере (k3d или minikube): Deployment, Service, Ingress, ConfigMap/Secret. Сделайте rolling update, убейте под и посмотрите на самовосстановление, отмасштабируйте API.
- **С агентом:** сгенерируйте манифесты из `compose.yaml` с помощью агента, затем проверьте вручную: пробы, лимиты, секреты.

## Результат
Манифесты (или Helm-чарт) + короткий ADR «нужен ли Slot'у Kubernetes?».
