---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Module 11: Governance, Safety & Team Adoption

## Norms, metrics, choosing a methodology

**Agentic Software Development: From Specs to Shipped Code**

---

<!-- Slide 2 -->

## Agenda

- Why this is a team decision, not a personal habit
- Disclosure norms — does a PR need an "AI-assisted" label?
- Review requirements by risk tier
- A decision framework: task type → methodology
- Metrics that actually tell you if this is working
- Common team-level failure modes
- Lab: build a one-page team policy + decision tree

---

<!-- Slide 3 -->

## Objectives

By the end of this module you can:

1. Draft a disclosure norm for agent-assisted commits/PRs
2. Set review requirements tied to risk tier, not gut feel
3. Build a decision tree: task type → required/recommended methodology
4. Pick metrics that catch a quality regression, not just a speed win
5. Recognize the three most common team-level failure modes early

---

<!-- Slide 4 -->

## From Individual Habit to Team Policy

- Modules 3–9 gave *you* five methodologies and the judgment to pick one
- A team doesn't get to rely on individual judgment alone:
  - reviewers need to know what bar applies *before* they open the diff
  - new hires need a default, not five options and no guidance
  - "it depends" is not a policy
- Module 11 turns personal judgment into a **written, followable norm**

> The goal isn't to remove judgment — it's to make the *default* explicit
> so judgment is spent on real edge cases, not on relitigating basics.

---

<!-- Slide 5 -->

## Disclosure Norms — The Core Question

- Does a PR need to say *"this was agent-assisted"*?
- Two failure directions:
  - **No disclosure at all** — reviewers apply human-pace assumptions to
    agent-paced output, miss things it wouldn't occur to them to check
  - **Disclosure with no consequence** — a label nobody acts on is just
    decoration
- The real question isn't "disclose or not" — it's **"what changes once
  we know?"**

---

<!-- Slide 6 -->

## Disclosure Norms — What a Working One Looks Like

A disclosure norm is only useful if it's *checkable* and *changes behavior*.

- **Checkable**: a PR template checkbox, a commit trailer
  (`Assisted-By: Claude Code`), or a required label — not "use your judgment"
- **Consequential**: disclosure triggers something concrete, e.g.
  - an extra reviewer for anything touching a high-risk path (Slide 8)
  - a shorter default review SLA is *not* granted
  - the PR description must name which methodology was used

*Undisclosed + later discovered agent-assisted work is a bigger trust
problem than the code itself — treat non-disclosure as the incident.*

---

<!-- Slide 7 -->

## Review Requirements by Risk Tier — Concept

- Not all code carries the same blast radius if agent-driven work goes wrong
- Tie review rigor to **what the change touches**, not to *how* it was made
- Same idea already exists without agents: a payments migration gets more
  eyes than a copy tweak — agents just make it more tempting to skip that
  scaling because the diff *looks* clean

---

<!-- Slide 8 -->

## Risk Tiers — A Starting Table

| Risk tier | Example paths | Minimum methodology | Review bar |
|---|---|---|---|
| High | auth, billing, data migrations, permissions | DDD or TDD + reviewer agent, human sign-off required | 2 human reviewers, no self-merge |
| Medium | shared libraries, public APIs, cross-team code | DDD or plan-first | 1 human reviewer, spec/plan attached |
| Low | internal tooling, prototypes, single-owner scripts | Conversational OK | 1 reviewer, async is fine |

*Tune the paths and headcounts to your repo — the shape (tiers → floor
methodology → review bar) is what transfers.*

---

<!-- Slide 9 -->

## A Decision Framework: Task Type → Methodology

- Reviewers ask "what changed" (risk tier). Authors need to ask
  "what kind of task is this" *before* they start
- Task type is a different axis than risk tier — a login-page CSS tweak
  is high-visibility but low-ambiguity; a new internal batch job is
  low-risk but highly ambiguous
- Both axes matter: task type picks the **methodology**, risk tier picks
  the **review bar** on top of it

---

<!-- Slide 10 -->

## The Methodology Comparison Matrix

| Methodology | Best for | Weak for | Artifact left behind |
|---|---|---|---|
| DDD (spec-first) | Features with real ambiguity, multi-person context | Tiny fixes (overhead) | Durable spec doc |
| Plan-first | Refactors, risky multi-file changes | Fast exploration | Ephemeral plan (or ADR) |
| TDD-with-agent | Bug fixes, well-defined logic | Vague/exploratory UI work | Test suite |
| Conversational | Prototypes, one-off scripts, exploration | Anything needing a paper trail | None (chat history only) |
| Multi-agent review | High-stakes changes, security-sensitive code | Low-stakes/small changes (overhead) | Review transcript |

*From the syllabus appendix — this is the raw material for today's lab.*

---

<!-- Slide 11 -->

## Turning the Matrix into a Decision Tree

```
Does the task touch a high-risk path (Slide 8)?
├─ YES → DDD or TDD, + multi-agent review, human sign-off
└─ NO
   └─ Is the requirement genuinely ambiguous / multi-person?
      ├─ YES → DDD (spec first)
      └─ NO
         └─ Is it a refactor or multi-file structural change?
            ├─ YES → Plan-first
            └─ NO
               └─ Is it a bug fix with a reproducible failure?
                  ├─ YES → TDD-with-agent
                  └─ NO → Conversational
```

- One tree, ~5 questions, walks any task to a default methodology

---

<!-- Slide 12 -->

## Decision Tree — Walked Through Twice

**Task A**: *"Add a retry with backoff to the billing webhook handler."*
→ touches billing (high-risk) → **DDD/TDD + multi-agent review**, sign-off required

**Task B**: *"Try three different empty-state illustrations on the
onboarding screen, we'll pick one."*
→ not high-risk, not ambiguous requirement, not a refactor, not a bug fix
→ **Conversational** — fastest path, no paper trail needed

*Same five questions, two very different — and correct — defaults.*

---

<!-- Slide 13 -->

## Metrics That Matter

Three signals, tracked **agent-assisted vs. human-only**, side by side:

- **Cycle time** — open-to-merge duration
- **Revert / rollback rate** — how often the change gets undone or hotfixed
- **Review comment volume** — how much reviewers actually had to say

Track all three together. Any one alone is misleading.

---

<!-- Slide 14 -->

## The Speed Trap

- Cycle time drops. Everyone's happy. Nobody looks further.
- Three months later: revert rate on agent-assisted PRs is 2–3x
  human-only, and review comment volume *per PR* has quietly fallen too
  — reviewers are skimming, not reading
- **Faster + more reverts = not actually faster** — count the rework
- A metrics dashboard with only cycle time is worse than no dashboard —
  it tells you a comforting lie with confidence

> If you only measure the thing agents are obviously good at (speed),
> you'll only ever learn that agents are fast.

---

<!-- Slide 15 -->

## A Minimal Metrics Review

- Pull cycle time, revert rate, and review-comment volume **monthly**,
  split by agent-assisted vs. human-only
- Watch for the pattern that matters: cycle time down **and** revert
  rate flat/down = real win; cycle time down **and** revert rate up =
  the speed trap, tighten review bar or methodology floor
- This isn't about banning agents when numbers dip — it's the feedback
  loop that lets you *adjust the policy* instead of guessing

---

<!-- Slide 16 -->

## Failure Mode 1 — Methodology by Habit

- A dev who had one good conversational session keeps using it for
  everything — including the auth change that needed DDD
- Symptom: the methodology used correlates with *who* wrote the PR, not
  *what* the PR touches
- Fix: the decision tree (Slide 11) removes the choice from vibes —
  the task type and risk tier decide, not the author's favorite mode

---

<!-- Slide 17 -->

## Failure Mode 2 — Specs Written and Never Updated

- A DDD spec gets written, the agent drifts from it mid-implementation,
  nobody updates the doc — now it actively misleads the next reader
- This is worse than no spec: a stale spec still *looks* authoritative
- Fix: the spec-update loop from Module 3 is a **policy requirement**,
  not a nice-to-have — PR template asks "does the spec still match?"

---

<!-- Slide 18 -->

## Failure Mode 3 — Review Fatigue

- Agents can produce review-ready-looking diffs much faster than a
  human review cadence can absorb them
- Reviewers start rubber-stamping — the review bar exists on paper but
  not in practice
- Fix: cap agent-assisted PRs per reviewer per day, or require the
  multi-agent reviewer pass (Module 8) to run *before* a human ever
  opens the diff, so humans review a pre-filtered set

---

<!-- Slide 19 -->

## Anatomy of a Team Policy Doc

A policy a new hire can follow with **no other context**:

1. **Disclosure norm** — how a PR states it was agent-assisted, and why
2. **Decision tree** — task description in, methodology out (Slide 11)
3. **Review requirements per risk tier** — the table from Slide 8
4. **Metrics** — what's tracked, how often, what triggers a policy review
5. **Known failure modes** — the three from Slides 16–18, named explicitly

*One page. If it doesn't fit on one page, it won't get read.*

---

<!-- Slide 20 -->

## Lab — Build Your Team Policy + Decision Tree

1. Start from the comparison matrix (Slide 10)
2. Build the decision tree (Slide 11 is a template, not the answer —
   adapt the questions to your team's actual task types)
3. Define your risk tiers and the review bar at each
4. Write one disclosure norm sentence that's checkable and consequential
5. Run 3 real recent task descriptions through your own tree — do the
   outputs feel right?

---

<!-- Slide 21 -->

## Deliverable

**The team policy doc** — one page, containing:

- The decision tree (task type → methodology)
- Review requirements by risk tier
- The disclosure norm

Bar to clear: *a new team member could follow it without having taken
this course.*

---

<!-- Slide 22 -->

## Recap & Next Module

- Governance turns individual judgment into a team default — judgment
  gets spent on real edge cases, not restated every PR
- Tie review rigor to risk tier; tie methodology to task type; disclose
  in a way that's checkable *and* consequential
- Measure cycle time, revert rate, and review volume **together**, or
  you'll only ever learn the flattering half of the story

**Next — Module 12: Capstone**
*Combine every methodology deliberately, on one real feature.*
