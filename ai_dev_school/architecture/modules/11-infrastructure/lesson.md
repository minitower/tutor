# Module 11 — Infrastructure for Your First Project

## Learning objectives
- Choose a hosting model for a project and estimate its cost
- Put an app on the internet on your own domain with HTTPS
- Make deployment, backups and monitoring automatic and reproducible

## Lecture outline
1. Hosting options: shared hosting, VPS, PaaS (Vercel, Render, Fly.io, Railway), IaaS cloud (AWS, GCP, Azure, Yandex Cloud, Selectel), serverless; control vs. effort vs. cost
2. VPS basics: SSH keys, a non-root user, firewall (ufw), automatic security updates, fail2ban
3. Domains and DNS: registrar, NS records, A/AAAA, CNAME, MX, TXT, TTL; how resolution works
4. HTTPS: TLS certificates, Let's Encrypt, automatic renewal
5. Reverse proxy: Nginx, Caddy, Traefik; one server, many services
6. Cloud building blocks: VPC and subnets, managed database, object storage (S3-compatible), CDN, load balancer, IAM
7. CI/CD: GitHub Actions → build image → push to registry → deploy; environments (staging/production)
8. Secrets: never in git; env files, CI secrets, secret managers
9. Backups: what, how often, where; a backup you never restored doesn't exist
10. Observability: logs, metrics, uptime alerts (Uptime Kuma, Grafana, Sentry for errors)
11. Infrastructure as code overview: Terraform/OpenTofu, Ansible; cost control and budget alerts

## Lab
Rent a VPS, point a domain at it, deploy "Slot" with Compose behind Caddy with HTTPS. Set up CI deploy on push to `main`, a nightly DB backup to object storage, and an uptime check.
- **With an agent:** ask the agent to write the CI workflow and a server hardening checklist; run every command yourself and never give the agent your production secrets.

## Deliverable
Live HTTPS URL + CI pipeline + proof of a successful restore from backup.
