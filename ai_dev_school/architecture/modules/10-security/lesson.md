# Module 10 — Security: Before the App Goes Public

## Learning objectives
- Threat-model an application: what is valuable, where the entry points are, who attacks
- Recognize and fix the most common web vulnerabilities (OWASP Top 10)
- Configure authentication, sessions, headers and secrets safely
- Build security checks into CI and keep dependencies under control

## Lecture outline
1. Why it matters now: bots scan every new site within minutes; security is a process, not a feature
2. Threat modeling: assets, entry points, attackers; STRIDE as a checklist; "Slot" assets — client phone numbers, the admin account, booking integrity
3. OWASP Top 10 (2025 edition) with "Slot" examples
4. Broken access control and IDOR: checking ownership on every request
5. Injection: SQL (parameterized queries), command injection; XSS and output escaping; Content Security Policy
6. CSRF, `SameSite` cookies and CORS — and what CORS does not protect
7. Authentication: password hashing (argon2id), login rate limits, MFA for admins, session and token lifetime, safe password reset
8. Security misconfiguration: debug mode, default passwords, open ports, verbose errors
9. Security headers: HSTS, CSP, `X-Content-Type-Options`, `frame-ancestors`, `Referrer-Policy`
10. Business-logic abuse: a bot booking every Friday slot; limits per phone and IP, confirmation, captcha on anomalies
11. Supply chain: lockfiles, `pip-audit` / `npm audit`, Dependabot/Renovate, image scanning, SBOM; "slopsquatting" — packages invented by AI
12. Personal data: minimization, encryption in transit and at rest, masking in logs, retention
13. Logging and alerting for security events; safe error handling (fail closed)
14. Security in CI: secret scanning, SAST, dependency and image scanning, DAST against staging
15. Security and AI agents: agent-written code gets the same review; agents may disable checks to make tests pass

## Lab
Write a one-page threat model for "Slot". On your own staging environment only, attack it with a partner: IDOR between two test users, SQL injection attempts, XSS through the review field, login brute force, mass booking by a script. Run an OWASP ZAP baseline scan. Fix every finding, add security headers, and add gitleaks, Semgrep, pip-audit/npm audit and Trivy to CI.
- **With an agent:** ask the agent to review the code against the OWASP checklist and to write tests that reproduce each vulnerability before the fix; verify every reported issue yourself — agents report false positives and miss real ones.

## Deliverable
The threat model, the attack log with fixes, a ZAP report before and after, and a CI pipeline with security checks.
