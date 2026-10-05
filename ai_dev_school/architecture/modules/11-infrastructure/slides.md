---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 11
## Infrastructure for Your First Project
### VPS, DNS, HTTPS, cloud, CI/CD, backups, monitoring — "Slot" on the internet

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- Where to host a project: hosting options
- A server from scratch: SSH, user, firewall
- Domains and DNS
- HTTPS and reverse proxies
- Cloud building blocks
- CI/CD: from push to production
- Secrets
- Backups
- Observability
- Infrastructure as code and money
- Lab

---

<!-- Slide 3 -->
## Learning objectives

- Choose a hosting model for a project and estimate the cost
- Put an app on the internet on your own domain with HTTPS
- Make deployment, backups and monitoring automatic
- Understand the building blocks of cloud infrastructure

---

<!-- Slide 4 -->
## Hosting options

| Option | What you get | Control | Your work | Starting price |
|---|---|---|---|---|
| Shared hosting | A folder for a PHP site | Minimal | Almost none | Pennies |
| **VPS** | A virtual server with root | Full | OS, security, updates | ~$5–10/mo |
| **PaaS** | "Give me code, I'll run it" | Medium | Just the code | Free–$20 |
| **IaaS cloud** | Building blocks: networks, VMs, DBs, storage | Full | A lot | From a few $ |
| **Serverless** | Functions per call | Minimal | Function code | Pay per call |

---

<!-- Slide 5 -->
## What to pick for a first project

- **Static frontend / Next.js** → PaaS (Vercel, Netlify, Cloudflare Pages) — free and fast
- **The whole app in Compose** → one VPS — cheap, clear, teaches you everything
- **Don't want to administer** → a container PaaS (Render, Fly.io, Railway)
- **Growing, need managed services** → a cloud (Yandex Cloud, Selectel, AWS, GCP)

For "Slot" in this course: **VPS + Docker Compose** — so you see every layer with your own hands.

---

<!-- Slide 6 -->
## A server from scratch: the first 15 minutes

```bash
# 1. Log in with an SSH key, not a password
ssh-copy-id root@203.0.113.10

# 2. A separate user
adduser deploy && usermod -aG sudo,docker deploy

# 3. Disable root and password login (/etc/ssh/sshd_config)
PermitRootLogin no
PasswordAuthentication no

# 4. Firewall: only SSH, HTTP, HTTPS
ufw allow OpenSSH && ufw allow 80,443/tcp && ufw enable

# 5. Automatic security updates
apt install unattended-upgrades fail2ban
```

---

<!-- Slide 7 -->
## Domains and DNS

- You buy a domain from a **registrar** (Reg.ru, Namecheap, Cloudflare)
- **NS records** say which DNS servers are responsible for the domain
- Those servers hold your records:

| Record | Example | Purpose |
|---|---|---|
| **A / AAAA** | `slot.example → 203.0.113.10` | Domain → IPv4 / IPv6 |
| **CNAME** | `www → slot.example` | An alias for another name |
| **MX** | `→ mx.yandex.net` | Where to deliver mail |
| **TXT** | `v=spf1 …`, verification | SPF/DKIM, proving ownership |

**TTL** — how many seconds an answer is cached. Lower the TTL well before a move.

---

<!-- Slide 8 -->
## How name resolution works

1. The browser asks a **recursive resolver** (your ISP, 1.1.1.1, 8.8.8.8, 77.88.8.8)
2. Resolver → **root server**: "who handles `.example`?"
3. → **the `.example` zone server**: "who handles `slot.example`?" → NS records
4. → **your DNS server**: "A record for `slot.example`?" → `203.0.113.10`
5. The resolver caches the answer for the TTL and returns it to the browser

Check it: `dig slot.example` or `nslookup slot.example`

---

<!-- Slide 9 -->
## HTTPS: why it's mandatory

- Without TLS anyone on the network (café Wi-Fi, the ISP) can read and tamper with traffic
- Browsers flag HTTP sites as "Not secure"
- Search engines rank HTTP sites lower
- Modern browser APIs (geolocation, PWA, service workers) work only over HTTPS

**Let's Encrypt** — free 90-day certificates with automatic renewal (certbot, Caddy, cert-manager).

---

<!-- Slide 10 -->
## Reverse proxy: one entry, many services

```
# Caddyfile — the HTTPS certificate is issued automatically
slot.example {
    handle /api/* {
        reverse_proxy api:8000
    }
    handle {
        reverse_proxy web:3000
    }
}
```

| Proxy | Strength |
|---|---|
| **Caddy** | Automatic HTTPS, a short config |
| **Nginx** | The classic, the most features and examples |
| **Traefik** | Finds containers by Docker labels on its own |

---

<!-- Slide 11 -->
## Cloud building blocks

| Block | What it is | Examples |
|---|---|---|
| **VPC, subnets** | Your isolated network | Every cloud |
| **VMs** | Virtual servers | Compute Cloud, EC2 |
| **Managed DB** | Turnkey PostgreSQL with backups and replicas | Managed PostgreSQL, RDS |
| **Object storage** | Files over HTTP, an S3-compatible API | Object Storage, S3 |
| **CDN** | A worldwide static cache | Cloud CDN, CloudFront |
| **Load balancer** | Spreading traffic | ALB, Network LB |
| **IAM** | Who may do what in the cloud | Service accounts, roles |

---

<!-- Slide 12 -->
## "Slot" once the project has grown

```
User → DNS → CDN (static)
           → Load balancer → 2+ API VMs (in a private subnet)
                               → Managed PostgreSQL
                               → Managed Redis
                               → Object Storage (files, backups)
```

- API servers have no public IPs — only the load balancer is exposed
- The DB is reachable only from the private subnet
- Everything is described in Terraform

---

<!-- Slide 13 -->
## CI/CD: from push to production

```yaml
# .github/workflows/deploy.yml
on: { push: { branches: [main] } }
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker compose run --rm api pytest
      - run: |
          echo "${{ secrets.GHCR_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker build -t ghcr.io/school/slot-api:${{ github.sha }} ./api
          docker push ghcr.io/school/slot-api:${{ github.sha }}
      - run: ssh deploy@slot.example "cd slot && TAG=${{ github.sha }} docker compose up -d"
```

**CI** — check every change. **CD** — automatically deliver what passed.

---

<!-- Slide 14 -->
## Environments

| Environment | Purpose | Data |
|---|---|---|
| **local** | Development | Test data |
| **staging** | Pre-release check, a copy of production | Anonymized |
| **production** | Real users | Real |

Rule: the same **image** goes staging → production; only environment variables differ.

---

<!-- Slide 15 -->
## Secrets

- **Never in git** — not even a private repo; bots find a leaked key within minutes
- `.env` in `.gitignore`; the repo has `.env.example` without values
- In CI — **CI secrets** (GitHub Actions secrets)
- In the cloud — a **secret manager** (Lockbox, Secrets Manager, Vault)
- A key leaked → **revoke it and issue a new one**, don't just delete the commit
- Give an agent only test keys, never production ones

---

<!-- Slide 16 -->
## Backups

- **What:** the DB (mandatory), uploaded files, configs
- **How:** scheduled `pg_dump` or the managed DB's built-in backups
- **Where:** **somewhere else** — object storage, another region
- **3-2-1 rule:** 3 copies, 2 different media, 1 off-site

> A backup you have never restored doesn't exist.

Once a month: restore a copy from backup and check the data is there.

---

<!-- Slide 17 -->
## Observability

| Signal | Question | Tools |
|---|---|---|
| **Logs** | What happened? | Loki, ELK, cloud logging |
| **Metrics** | How many and how fast? | Prometheus + Grafana |
| **Traces** | Where is the request slow? | OpenTelemetry, Jaeger |
| **Errors** | What broke for the user? | Sentry |
| **Uptime** | Is the site up at all? | Uptime Kuma, external pingers |

Minimum for a first project: **an uptime check with a Telegram alert + Sentry**.

---

<!-- Slide 18 -->
## Infrastructure as code

```hcl
resource "yandex_compute_instance" "app" {
  name        = "slot-app"
  platform_id = "standard-v3"
  resources {
    cores  = 2
    memory = 4
  }
  boot_disk { initialize_params { image_id = "fd8…ubuntu-24-04" } }
  network_interface { subnet_id = yandex_vpc_subnet.private.id }
}
```

- **Terraform / OpenTofu** — describe cloud resources: `plan` shows changes, `apply` applies them
- **Ansible** — configure servers: packages, users, configs
- Infrastructure is reproducible, reviewed in PRs, not "set up by hand at some point"

---

<!-- Slide 19 -->
## Money

- Turn on **budget alerts** in the cloud on day one
- Typical leaks: forgotten VMs and disks, egress traffic, NAT gateways, logs with no retention limit
- Start small and scale by metrics, not "for future growth"
- Free tiers have limits — read the terms

---

<!-- Slide 20 -->
## Lab

1. Rent a VPS, set up SSH keys, a user, a firewall
2. Buy a domain (or use a subdomain), point an A record at the VPS
3. Deploy "Slot" with Compose behind Caddy with HTTPS
4. Set up deploy from GitHub Actions on push to `main`
5. A nightly DB backup to object storage — **and restore from it**
6. An uptime check with an alert
7. **With an agent:** ask the agent to write the CI workflow and a server hardening checklist; run the commands yourself, never give the agent production secrets

---

<!-- Slide 21 -->
## Deliverable

- A live `https://…` address with a valid certificate
- A CI pipeline: tests → image → deploy
- Proof of a successful restore from backup
- A screenshot of a downtime alert (stop the API and wait for the notification)

---

<!-- Slide 22 -->
## Recap and next module

- First project: VPS + Compose or a PaaS; the cloud when you need managed services
- DNS turns a name into an address; HTTPS is mandatory; a reverse proxy is the single entry point
- CI/CD, secrets outside git, tested backups, monitoring — from day one
- Next: **Module 12 — Launch & Growth**: how users will find "Slot"
