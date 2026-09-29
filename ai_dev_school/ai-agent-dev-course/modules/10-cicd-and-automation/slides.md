---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 10: CI/CD & Automating Agent Workflows

## Agents as pipeline citizens

**Agentic Software Development: From Specs to Shipped Code**

---

<!-- Slide 2 -->

## Agenda

- Why put an agent *inside* a pipeline at all
- Hooks: git hooks vs. Claude Code hooks vs. CI hooks
- Scheduled and triggered agents
- Agents-in-CI patterns: lint auto-fix, issue triage, release notes
- Permission scopes and sandboxing for unattended agents
- Designing a human-in-the-loop gate with no human watching live
- Lab: wire an agent into one CI step or git hook, with a gate

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

1. Explain the difference between an interactive agent session and an
   agent triggered by an event or a schedule
2. Name at least three agents-in-CI patterns and the risk profile of each
3. Design permission scopes and a sandbox for an unattended agent
4. Design an approval gate that works with no human watching in real time

---

<!-- Slide 4 -->

## From Co-pilot to Pipeline Citizen

- So far in this course: a human runs the agent, watches, approves each step
- In CI/CD, nobody is watching turn-by-turn — the agent runs **unattended**
- Same loop from Module 1 (plan → act → observe → repeat), new constraint:
  - no one to catch a bad decision *before* it takes effect
- The whole module is one question: **what changes when nobody's watching?**

---

<!-- Slide 5 -->

## The Core Tension

| Interactive session | Unattended pipeline agent |
|---|---|
| You approve each risky action live | Nobody is present to approve live |
| Mistakes are caught in seconds | Mistakes may ship before anyone looks |
| Trust is built turn by turn | Trust must be designed in *up front* |

> Unattended does not mean unsupervised — supervision just moves from
> "live human" to "designed boundary."

---

<!-- Slide 6 -->

## Hooks: Three Different Things Share One Name

- **Git hooks** — scripts your local git runs on an event (`pre-commit`,
  `pre-push`) — run on the developer's machine
- **Claude Code hooks** — shell commands the *agent harness* runs around
  tool calls (`PreToolUse`, `PostToolUse`, `Stop`, …) — enforce policy
  regardless of what the agent decides to do
- **CI hooks** — a pipeline step triggered by a repo event
  (`on: pull_request`, `on: issues`) — run on a CI runner, not your laptop

---

<!-- Slide 7 -->

## Git Hook Example

`.git/hooks/pre-commit` (or via a framework like `pre-commit`/`husky`):

```bash
#!/usr/bin/env bash
# Block the commit if an agent left a WIP marker or a secret-looking string
if git diff --cached | grep -qE 'TODO\(agent\)|AKIA[0-9A-Z]{16}'; then
  echo "Blocked: unresolved agent marker or possible secret in staged diff"
  exit 1
fi
```

- Runs before code ever leaves the machine — cheapest place to catch a mistake
- Can't be skipped by the agent unless the agent controls the hook itself
  (never let it)

---

<!-- Slide 8 -->

## Claude Code Hook Example

`.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command",
            "command": "scripts/block-dangerous-bash.sh" }
        ]
      }
    ]
  }
}
```

- Enforced by the harness, **outside** the model's control — the agent
  cannot reason its way past a hook that denies the call
- This is the mechanism, not the policy — Slides 13–15 cover what to deny

---

<!-- Slide 9 -->

## Scheduled Agents

- Run on a timer, no triggering event — e.g. nightly dependency audit,
  weekly stale-issue sweep

```yaml
# .github/workflows/nightly-audit.yml
on:
  schedule:
    - cron: "0 3 * * *"
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude -p "Audit dependencies for known CVEs; open an issue
                         per finding. Do not open PRs."
```

- Output is scoped to something safe-by-construction: an issue, not a merge

---

<!-- Slide 10 -->

## Triggered Agents

- Run in response to a specific repo event, not a clock

```yaml
# .github/workflows/lint-fix.yml
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  lint-fix:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: claude -p "Run the linter; fix only lint violations;
                         commit as 'lint: auto-fix' on this branch."
```

- Event-scoped = agent only ever sees the diff relevant to *this* PR

---

<!-- Slide 11 -->

## Pattern 1 — Auto-Fix Lint

- Trigger: PR opened/updated → run linter → agent fixes violations only
- Safe by construction *if* scoped tightly:
  - only touches lines the linter flagged
  - commits to the PR's own branch, never `main`
  - a failing auto-fix just leaves the lint error for a human, it doesn't
    block anything further
- Still needs review before merge — an auto-fix is a proposal, not a fact

---

<!-- Slide 12 -->

## Pattern 2 — Issue Triage

- Trigger: `on: issues: [opened]` → agent labels, deduplicates, asks
  clarifying questions, links related issues/PRs
- Never: closes issues, assigns humans without asking, edits titles in
  ways that lose the reporter's original wording
- High leverage, low risk — worst case is a wrong label, which is cheap
  to fix and doesn't touch code or data

---

<!-- Slide 13 -->

## Pattern 3 — Draft Release Notes

- Trigger: tag pushed / release branch cut → agent drafts notes from
  commit messages and merged PR titles
- The verb is **draft** — output lands as a PR to `CHANGELOG.md` or a
  draft GitHub Release, never an email, Slack post, or published release
- Publishing/sending is a *separate*, human-triggered step — always

---

<!-- Slide 14 -->

## Permission Scopes for Unattended Agents

- An unattended agent's permissions should be **narrower** than an
  interactive session's, not the same
- Ask for every capability separately — don't hand out "admin" by default:
  - repo write? which branches?
  - can it comment on issues/PRs? can it merge?
  - does it have any credential that reaches outside the repo (Slack,
    email, cloud billing, prod DB)?
- Default answer to each: **no**, until a specific task justifies it

---

<!-- Slide 15 -->

## The Never-Without-a-Gate List

Never allow an unattended agent to do these **without an explicit human
approval step**, no matter how convenient:

- `git push --force` (rewrites history other people rely on)
- delete data (drop a table, `rm` outside its working tree, close/delete
  an issue thread)
- send anything external (email, Slack, a published release, a tweet)
- spend money (cloud spend, paid API calls beyond a small fixed budget)

*These are exactly the actions a mistake can't be undone by re-running.*

---

<!-- Slide 16 -->

## Sandboxing — Limiting the Blast Radius

- Run the agent in a throwaway environment, not shared infrastructure:
  - ephemeral CI runner / container, destroyed after the job
  - a service account scoped to *this repo*, not the whole org
  - no production credentials in the job's environment at all
- Sandboxing is a second layer, not a replacement for the never-list —
  it limits damage *if* a permission boundary is misconfigured

```yaml
permissions:
  contents: write     # this repo only
  pull-requests: write
  # no `issues: write` if this job never needs it — omit, don't just ignore
```

---

<!-- Slide 17 -->

## Designing the Gate: No Human Watching Live

- "Approval" without a live human means the gate has to be **structural**,
  checked automatically, not a person clicking "yes" in the moment
- Working patterns:
  - **required PR review** — the agent can open the PR, a human (or a
    review policy: 1 approval, CODEOWNERS) must approve before merge
  - **draft-only output** — the agent's artifact is inert until a human
    promotes it (draft release, draft PR, unsent changelog)
  - **branch protection** — `main` requires status checks + review, so
    even a compromised agent identity can't merge around it

---

<!-- Slide 18 -->

## Gate Example: Branch Protection + Required Review

```yaml
# repo settings (illustrative, not literal YAML you paste in)
branch_protection:
  main:
    required_pull_request_reviews:
      required_approving_review_count: 1
      require_code_owner_reviews: true
    restrict_pushes: true       # no direct pushes, agent included
    required_status_checks: [lint, tests]
```

- The gate lives in **repo config**, not in the agent's prompt — a prompt
  saying "ask before merging" is a suggestion; branch protection is a wall

---

<!-- Slide 19 -->

## Anti-Patterns to Avoid

- **Agent reviews its own PR** — same identity opening and approving
  defeats the gate entirely
- **Broad token, narrow prompt** — "just don't force-push" in the prompt,
  while the credential *can* force-push — the boundary must be enforced
  where the agent can't argue with it
- **Silent auto-merge** — any path where "tests passed" alone merges to
  `main` with no review step removes the gate you just designed
- **One shared bot credential for everything** — one compromised job now
  has every permission every job ever needed

---

<!-- Slide 20 -->

## Lab — Wire an Agent into a Pipeline

Pick **one**:
- Auto-fix lint on PR open, committed to the PR branch, human-reviewed
  before merge
- Draft a `CHANGELOG.md` entry from commits since the last tag, opened
  as a PR, never auto-merged

Requirements:
1. A working config (CI workflow file, or a git hook + script)
2. A concrete, explicit approval gate before anything destructive or
   externally visible

---

<!-- Slide 21 -->

## Deliverable

- The working pipeline config (workflow YAML / hook script)
- A short written note listing what this automation is **not** allowed
  to do unattended — and *why* each boundary was chosen
  - tie each boundary back to Slide 15's never-list or a project-specific
    risk you identified

---

<!-- Slide 22 -->

## Recap & Next Module

- Unattended agents need boundaries **designed in**, not assumed —
  hooks, scopes, and sandboxes are the mechanism
- Draft, don't send. Propose, don't merge. Structural gates beat prompt
  instructions every time
- The never-list (force-push, delete, send, spend) applies regardless of
  how convenient skipping it would be

**Next — Module 11: Governance, Safety & Team Adoption**
*Turning individual guardrails into team-wide norms.*
