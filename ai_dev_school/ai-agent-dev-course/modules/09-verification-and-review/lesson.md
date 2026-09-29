# Module 9 — Verification & Review of Agent Output

## Learning objectives
- Build the habit of verifying agent output before trusting it, matched
  to the risk of what changed
- Recognize agent-specific failure modes that don't show up in normal
  human-authored-code review checklists

## Key concepts
- Hallucinated APIs: agent calls a function/library method that doesn't
  exist, or exists with different behavior than assumed — usually caught
  by actually running the code, not just reading it
- Silent scope creep: the agent "helpfully" changes things outside the
  requested scope; review diffs for size and surface area, not just
  correctness
- Security review for AI-generated code: same OWASP-class concerns as
  human code, plus checking that the agent didn't take a shortcut (e.g.
  string-concatenated SQL) to satisfy a test quickly
- Prompt-injection risk: if the agent reads untrusted content during the
  task (a web page, a ticket, a file from outside the repo), that content
  can contain instructions aimed at the agent, not at you — review for
  this specifically when tasks involve external data

## Lab
Take code produced in an earlier module's lab. Run a structured review
pass: correctness against acceptance criteria, scope check against the
original request, and a security pass (input handling, secrets, injected
instructions if any external content was involved).

## Deliverable
A filled-out review checklist plus findings — including "found nothing"
if that's the honest result.
