# Module 13 — Lecture Script: CI/CD & Automating Agent Workflows

*Speaking notes for the instructor. Slide numbers match `slides.md` exactly.
Timing notes are cumulative suggestions for a live 2–2.5 hour session
(lecture + lab). Adjust to your room.*

---

## Opening & Framing (Slides 1–5) — ~15 min

### Slide 1 — Module 13: CI/CD & Automating Agent Workflows

Welcome back. Every module so far has had you in the loop, in real time —
you type a task, the agent works, you watch the diff come in, you approve
or correct it. That's Modules 1 through 12 in one sentence. Today we take
the human out of that loop, on purpose, for specific kinds of work, and we
ask the question that makes people nervous the first time they hear it:
what happens when an agent runs and nobody's watching?

That's the case-study focus for this module — agents as pipeline citizens.
Not "agent as your pair programmer," but "agent as one more automated step
in your CI/CD pipeline," sitting next to your linter, your test runner,
your deploy job. Same repo, same trust boundaries that already exist for
every other piece of automation you run unattended — we're just extending
those boundaries to cover a much more capable, much less predictable actor.

### Slide 2 — Agenda

Quick tour of where we're going. We'll start with hooks, and I want to
warn you up front — that word means three genuinely different things
depending on context, and conflating them is the single most common
confusion I see. Then scheduled and triggered agents — the "when does it
even run" question. Then three concrete agents-in-CI patterns you can
lift almost directly into a real repo. Then the two mechanisms that make
any of this safe: permission scopes and sandboxing. Then the hardest part
conceptually — designing an approval gate for a process where no human is
watching live. And we close with the lab, where you build one small piece
of this yourself.

### Slide 3 — Objectives

By the end of today you should be able to do four things, and I'll come
back to check each one before we're done. First: articulate clearly what
changes between an interactive session — everything you've done so far in
this course — and an agent that's triggered by an event or a clock.
Second: name at least three agents-in-CI patterns and tell me, for each
one, what's the worst thing that could realistically go wrong. Third:
actually design permission scopes and a sandbox for an agent that has no
one watching it. And fourth — the one that tends to be hardest — design
an approval gate that functions correctly with nobody available to click
"approve" in the moment.

### Slide 4 — From Co-pilot to Pipeline Citizen

Let's name the shift explicitly, because it's easy to let it slide past
you. In every lab up to now, the loop from Module 1 — plan, act, observe,
repeat — has run with you as an active participant. You're the observer
of last resort. If the agent is about to do something dumb, you catch it
in the two or three seconds before it happens, because you're reading the
tool-call output as it streams by.

In a CI/CD context, that observer is gone. The agent still runs the exact
same loop internally — nothing about *how it thinks* changes — but the
feedback loop that used to include you now has to be entirely mechanical.
So here's the framing question I want you to hold in your head for the
rest of this module: **what changes when nobody's watching turn by turn?**
The honest answer is: nothing about the agent changes. Everything about
the *harness around it* has to change.

### Slide 5 — The Core Tension

This table is the whole module compressed into three rows, so let's sit
with it for a second. Interactive: you approve risky actions live, live
means the error-correction time is measured in seconds, and trust gets
built turn by turn as you watch the agent behave reasonably. Unattended:
there's no live approval, an error can ship — get merged, get sent,
cost money — before a human so much as glances at it, and trust can't be
built turn by turn anymore because there's no "turn" a human is present
for.

Read that pull quote again: unattended doesn't mean unsupervised. It
means supervision has to move from a person to a *designed boundary* —
something that exists in config, in repo settings, in a sandboxed
environment, before the agent ever runs. If you remember one sentence
from this whole lecture, make it that one. Everything else today is just
worked-out detail underneath it.

---

## Hooks (Slides 6–13) — ~15 min

### Slide 6 — Hooks: Three Different Things Share One Name

Here's where I want to slow down, because "hook" is genuinely overloaded
and if you walk away from this module using the word loosely, you'll
confuse your teammates in exactly the way people confused *you* the first
time someone said "just add a pre-commit hook" and you weren't sure if
they meant a script, a framework, or a GitHub Action.

Three distinct things:

Git hooks are the oldest of the three — plain scripts that your local git
binary runs automatically at specific points: before a commit is created,
before a push leaves your machine, after a checkout. They run on the
*developer's own machine*, which matters a lot for what they can and
can't guarantee — more on that in a second.

Claude Code hooks are a newer, different mechanism — shell commands that
the *agent harness itself* runs at specific points around tool calls.
Events like `PreToolUse` — before the agent's tool call is allowed to
execute — `PostToolUse`, `Stop`, and a few others. The key distinguishing
feature: this is enforced by the harness, not by the model. The agent
doesn't get a vote.

CI hooks — and this is a slight abuse of the word "hook," but people say
it anyway — are pipeline steps triggered by a repository event: a PR
opened, an issue filed, a tag pushed. These run on a CI runner somewhere
in the cloud, not on anyone's laptop.

Why does the distinction matter practically? Because each one has a
different threat model. A git hook can be bypassed with `--no-verify` by
anyone with local access. A Claude Code hook can't be argued around by
the model, but it *can* be misconfigured by whoever writes the hook
script. A CI hook runs somewhere you don't fully control the environment
of, which is exactly why sandboxing — Slide 24 — matters so much for that
third category.

### Slide 7 — Git Hook Example

Let's look at a concrete one. This is a `pre-commit` script — you'd drop
this at `.git/hooks/pre-commit`, or more realistically wire it up through
a framework like the `pre-commit` tool or `husky` so it's shared across
your team instead of living only on your machine.

Walk through what it does: it looks at the staged diff — everything about
to become a commit — and greps for two danger signals. One is a literal
marker string, `TODO(agent)`, which is a convention some teams adopt so
an agent can flag "I wasn't sure about this line" without silently
guessing. The other is a pattern that looks like an AWS access key —
`AKIA` followed by sixteen alphanumeric characters. If either shows up,
the commit is blocked with a nonzero exit code, and the developer — or
the agent, if it's the one calling `git commit` — has to deal with it
before anything gets committed at all.

Why is this the cheapest place to catch a mistake? Because nothing has
left the machine yet. No CI minutes spent, no PR opened, no reviewer's
attention consumed. It's the tightest possible feedback loop. And the
caveat that matters: this only holds if the agent doesn't control the
hook itself. If an agent has write access to `.git/hooks/`, it could —
even unintentionally, while "cleaning up" a repo — disable its own
guardrail. So: hooks live in version-controlled config the agent doesn't
get to edit unsupervised, full stop.

### Slide 8 — Claude Code Hook Example

Now the second flavor. This is a snippet from `.claude/settings.json` —
the config file that shapes how the Claude Code harness behaves in this
repo. We're registering a `PreToolUse` hook: before any `Bash` tool call
is allowed to execute, run this shell script first, and let its exit code
decide whether the call proceeds.

The script referenced here, `block-dangerous-bash.sh`, is something your
team writes — pattern-matching against command strings you never want
executed automatically: `rm -rf`, `git push --force`, `curl` piping into
`sh`, whatever your organization's danger list looks like.

Here's the sentence I want you to underline: this is enforced by the
harness, outside the model's control. The model can be as confident as it
wants that force-pushing is fine in this instance — it doesn't get to
negotiate with a hook. The hook either allows the call or it doesn't.
That's a fundamentally different guarantee than "the system prompt says
not to do this," which is a request the model can, in principle,
misjudge or override under enough context pressure.

I'm deliberately not prescribing exactly what goes in that denylist right
now — that's policy, not mechanism, and we get to the policy question in
detail on Slides 21 through 23. Today, just fix the mechanism in your
head: hooks are how you make a rule *true regardless of what the agent
decides*, rather than a rule you're hoping the agent respects.

---

### Slide 9 — When an Agent System Needs Claude Code Hooks

The most common question after the hooks slides: "when do I actually
need this, if I can write a rule in CLAUDE.md?" Simple answer. In an
interactive session a human is next to the agent, sees a suspicious
command and clicks "deny". In CI, where the agent runs as `claude -p`,
nobody is there. So anything that must be *always true* has to rest on a
mechanism, not on a request.

Walk the table top to bottom. A ban on dangerous commands is
`PreToolUse`: it fires before the call and can block it. Auto-format
after edits is `PostToolUse`: you're not hoping the agent remembers the
formatter. "Don't say done while tests are red" is `Stop`. The audit log
is the same `PostToolUse`, just writing to a file. Style and preferences
are not hooks — that's an ordinary instruction in `CLAUDE.md`: if the
agent slips once, nothing terrible happens.

The one-line rule: irreversible, or must be 100% — hook; a preference —
instruction.

### Slide 10 — How to Add a Hook to a Project

The mechanics in three steps. First, write a script. The harness passes
it JSON on stdin: the tool name and its arguments — for `Bash`, the
command. Second, register the script in a config. There are three
places: `.claude/settings.json` lives in the repo and is shared by the
team — policy goes here; `.claude/settings.local.json` is personal and
stays out of git; `~/.claude/settings.json` applies in all your
projects. Third, make the script executable and commit it.

The slide's example wires three hooks: `PreToolUse` on `Bash` — blocks
dangerous commands; `PostToolUse` on `Edit|Write` — runs the formatter
after every edit; `Stop` — runs tests before the agent claims it's
finished. `matcher` filters by tool name and is a regular expression.

### Slide 11 — A Hook Script: Blocking the Dangerous

Here's the script itself. It reads the JSON, extracts the command with
`jq`, checks it against a blacklist and exits with a code. The exit-code
convention is simple: zero — allow, two — block. The most useful
property of a block: whatever you write to `stderr`, the harness hands to
the *agent*. So make the message human: what was blocked and what to do
instead. The agent reads it and proposes a safe path instead of
banging on the wall.

A separate note on the `Stop` hook. If it exits with 2, the agent can't
finish and gets the output — usually failing tests. Elegant, but easy to
loop: if the tests can't be fixed, the agent spins forever. So check the
`stop_hook_active` field in the input JSON and skip a repeat run.

### Slide 12 — How to Design Hooks

Five principles. First: start from policy, not from a script. You
already have a never-list; each line must become either a hook or a
permission restriction. Second: a hook is deterministic code. No model
calls inside: it must run in fractions of a second and always the same
way.

Third — what to do when the hook itself errors. For a dangerous action,
closing is safer: couldn't parse the input — block. For conveniences like
a formatter, do the opposite: let it pass; no reason to stop work
because `ruff` crashed. Fourth — the `stderr` message: the agent reads
it, so write it so the agent can correct itself.

And fifth, honestly: a blacklist is brittle. A command can be wrapped in
`sh -c`, base64-encoded, written in another language. So a hook is one
layer, and permissions and a sandbox must stand next to it.

### Slide 13 — Testing and Protecting Hooks

A hook is policy code, so it deserves tests like any other code. The
test is simple: run the script, feed it JSON with a dangerous command
and check the exit code — two. Then a safe one — zero. Two such tests
catch the most annoying mistake: you "set up protection" and the regex
actually catches nothing.

The other half of the slide is who guards the guard. If the agent may
write to `.claude/` or `scripts/hooks/`, it can disable its own hook,
even without malice, "tidying up". So those paths go in `CODEOWNERS` and
writes to them are denied for the agent. And log the triggers: if a hook
blocks the same command ten times a day, that's a reason to rethink the
task or the prompt.

---

## Scheduled and Triggered Agents (Slides 14–15) — ~10 min

### Slide 14 — Scheduled Agents

Moving from "how do we enforce a boundary" to "what actually kicks the
agent off in the first place." Scheduled agents run on a timer, with no
particular event causing them — a cron expression, essentially. The
example on screen is a nightly dependency audit: at 3 AM every day, a
GitHub Actions workflow checks out the repo and asks Claude to scan
dependencies for known CVEs and open an issue per finding.

Notice the last clause in that prompt: "Do not open PRs." That's not
incidental — it's load-bearing. Scheduled jobs run with nobody around to
notice if the output is wrong at 3 AM, so whatever the job produces needs
to be safe-by-construction. An issue is a great output for an unattended
job: it's inert. Nobody's code changes because an issue got filed. Worst
case, someone triages a bad issue in the morning and closes it. Compare
that to a scheduled job that opens *and merges* PRs — now a 3 AM mistake
is live in your codebase before anyone's had coffee.

Other good candidates for scheduled agents: a weekly sweep for stale
issues that proposes closing them (proposes — doesn't close), a monthly
audit of unused feature flags, a nightly summary of failing tests across
branches. Notice the pattern across all of these — the output is always
a report or a proposal, never a direct mutation of something that
matters.

### Slide 15 — Triggered Agents

Triggered agents are the other half of "how does it start" — instead of
a clock, a specific repository event fires the job. Here it's `on:
pull_request` with types `opened` and `synchronize`, meaning: run this
every time a PR is opened, and every time new commits land on it. The
job checks out the code and asks Claude to run the linter and fix only
what it flags, then commit that fix to the PR's own branch.

The phrase I want you to notice is "event-scoped." Because this job only
fires in the context of one specific PR, the agent's entire field of view
is naturally the diff relevant to *that* PR — it's not going to wander
off and "helpfully" touch unrelated files across the repo, because the
checkout it's working in is exactly this branch, exactly this PR's
state. That's a nice, mostly-free safety property that comes from how the
trigger is scoped, before you've even written a single line of
permission policy. It won't save you from an agent doing something
harmful *within* the scope of that PR, but it does bound the blast radius
to "one PR" instead of "the whole repository," which is worth quite a
lot.

Quick contrast to hold onto: scheduled agents answer "when, on a clock,"
triggered agents answer "when, in response to what." Most of the patterns
we're about to walk through are triggered, because most CI work is
naturally event-driven — a PR is opened, an issue is filed, a tag is
pushed.

---

## CI/CD Platforms (Slides 16–18) — ~10 min

### Slide 16 — CI/CD Platforms: GitHub Actions and Alternatives

So far every example used GitHub Actions, but the idea isn't tied to
it. Any CI system does the same thing: on an event it spins up a clean
environment and runs commands. The agent is just one more command:
`claude -p` in headless mode takes a prompt and prints a result with no
interactive dialogue.

The table lists the five most common platforms. GitHub Actions also has
a ready-made action from Anthropic, `anthropics/claude-code-action`, but
a plain `run: claude -p` works too. What really differs between
platforms is the config file, the set of events, and how secrets and
token permissions are issued. Choose the one where your repo already
lives: no need to migrate for the agent.

### Slide 17 — The Same Agent in GitLab CI

To see what transfers one-to-one — the same agent, but in
`.gitlab-ci.yml`. Instead of `on: pull_request` there's a `rules` block
with `merge_request_event`. Instead of `runs-on` — `image`. The command
is the same: `claude -p`.

Note the three limiters. `timeout` caps time. `--max-turns` caps the
agent's steps. `--allowedTools` — the agent can only read. The MR
comment is posted by a separate step with a narrow token. The API key
lives in a masked and protected CI variable, not in the repo. These are
the same principles as on GitHub: boundaries are set by configuration,
not by the prompt.

### Slide 18 — Common Requirements for an Agent on Any CI Platform

Whatever you pick, the checklist is one. Secrets — only in protected
variables. The job token is minimal; where the platform supports OIDC,
use it instead of long-lived cloud keys.

Separately — PRs from forks. A foreign PR is untrusted code and text,
exactly the content prompt injection from Module 12 is made of. So
secrets aren't passed to those runs, and `pull_request_target` on
GitHub, which runs in the main repo's context, with foreign code is a
direct road to an incident.

And limits: timeout, step count, `concurrency` so one PR doesn't start
two agents, and an API budget. And keep the agent's log and output as
an artifact — without it there's nothing to investigate.

---

## Agents-in-CI Patterns (Slides 19–21) — ~15 min

### Slide 19 — Pattern 1: Auto-Fix Lint

This is probably the single most common agents-in-CI pattern in the wild
right now, so let's get it exactly right. Trigger: PR opened or updated.
Action: run the linter, then let the agent fix *only* the violations the
linter actually flagged — not "clean up the file while you're in there,"
just the specific complaints.

Three things make this safe by construction, and I want you to notice
they're all about *scope*, not about trusting the agent's judgment more.
One: it only touches the lines the linter identified — a narrow,
mechanically-defined edit surface. Two: it commits to the PR's own
branch, never to `main` — so even a bad auto-fix is sitting in a branch
that still needs review and a merge to matter. Three — and this one
people forget — a *failed* auto-fix attempt just leaves the original
lint error sitting there for a human to deal with. It doesn't block the
pipeline, it doesn't retry destructively, it just... doesn't help, which
is a perfectly acceptable failure mode.

And here's the sentence that ties back to Module 12: an auto-fix is a
proposal, not a fact. It still needs review before merge, same as any
other change to the codebase. The fact that a machine wrote it doesn't
lower the bar — if anything, given what we covered on hallucinated
behavior in Module 12, it might raise it slightly, at least until your
team has a track record with this specific automation.

### Slide 20 — Pattern 2: Issue Triage

Second pattern, and notice the risk profile is genuinely different from
the first. Trigger: a new issue is opened. Action: the agent labels it,
checks for likely duplicates, asks the reporter clarifying questions if
the report is too vague to act on, and links related issues or PRs it
finds.

What's explicitly off the table: closing issues outright, assigning a
human without that human's buy-in, or rewriting the reporter's original
title or description in a way that loses their actual words. Why those
three specifically? Because each one either removes information (closing,
overwriting the title) or creates an obligation on a person who didn't
consent to it (an assignment).

Here's why I put this pattern right after lint auto-fix even though
they're quite different: issue triage is a great example of "high
leverage, low risk," and it's worth understanding *why* it's low risk,
because that reasoning is reusable. The worst realistic outcome of a bad
triage is a wrong label. That's cheap — someone fixes it in five seconds
— and critically, it never touches code, never touches data, never
leaves the tracker. Compare that to lint auto-fix, where the worst case
at least touches source code, even if it's gated by review. Ranking
agents-in-CI patterns by "what's the actual blast radius of the worst
case" is a habit I want you to build, and we'll use it again on the
never-list in a few slides.

### Slide 21 — Pattern 3: Draft Release Notes

Third pattern, and this one exists specifically to teach a vocabulary
distinction that matters for the rest of the module. Trigger: a tag gets
pushed, or a release branch is cut. Action: the agent reads commit
messages and merged PR titles since the last release and drafts release
notes from them.

The operative word on this slide, in bold, is **draft**. Where does the
output land? A PR against `CHANGELOG.md`, or a draft GitHub Release — the
kind that sits there, visible only to people with repo access, until
someone with authority clicks "publish." What it never does is become an
email newsletter, a Slack announcement to the whole company, or a
publicly published release note. Those are fundamentally different
actions with fundamentally different reversibility — you can edit a PR a
hundred times before merging it; you cannot un-send an email to your
entire user base.

This is the cleanest illustration in the whole module of a principle
we'll state explicitly in a few slides: publishing or sending is *always*
a separate, human-triggered step, no matter how good the draft is, no
matter how many times the agent has gotten it right before. The agent's
job ends at "here's a draft, ready for your eyes." A person's job begins
at "I've read it and I'm choosing to make it public."

---

## Permission Scopes and Sandboxing (Slides 22–24) — ~15 min

### Slide 22 — Permission Scopes for Unattended Agents

We've now seen three patterns; let's get precise about the mechanism
that keeps them safe, because "safe by construction" isn't magic, it's
permission scoping done deliberately.

Core claim on this slide: an unattended agent's permissions should be
*narrower* than an interactive session's — not equal to it. That might
feel backwards at first; you might assume a well-tested, repeatable CI
job deserves more trust than an ad hoc interactive session. But it's the
opposite, because in an interactive session, you're the safety net for
every single action, in real time. In a CI job, there is no safety net
except what you configured in advance. The job needs to be trustworthy
enough to run with *no* net.

So: ask for every capability separately, and default every answer to
"no." Does it need repo write access — and if so, which branches
specifically? Does it need to comment on issues or PRs? Can it merge — and
I'd bet for almost every pattern we've discussed today, the honest answer
is no, it should never be able to merge itself. Does its credential reach
outside the repo at all — a Slack webhook, an email-sending API key,
anything that touches cloud billing or a production database? If the
task doesn't specifically require one of these, don't grant it "just in
case." Every capability you grant "just in case" is a capability that's
sitting there the day something goes wrong.

### Slide 23 — The Never-Without-a-Gate List

This is the list I want you to actually memorize — not paraphrase, not
approximately recall, memorize — because it's short enough to memorize
and it will make you look extremely competent in a design review.

Four categories, never allowed unattended, no matter how convenient it
would be: force-pushing, because it rewrites history other people have
already built on top of — someone else's local branch, a deployed
artifact referencing a specific commit, a CI run that already validated
a specific SHA. Deleting data — dropping a table, an `rm` that reaches
outside the agent's intended working tree, closing or deleting an issue
thread that had useful history in it. Sending anything external — email,
a Slack message, a published release, a tweet — anything that leaves
your infrastructure and reaches a human who didn't ask an agent to
contact them. And spending money — cloud spend, paid API calls beyond
some small, fixed, pre-approved budget.

Notice the common thread, spelled out in the italic line at the bottom:
these are exactly the actions where a mistake can't be undone by
re-running the job. Everything else we've discussed today — a bad lint
fix, a wrong label, a rough draft changelog — costs you a few minutes to
notice and correct. These four categories cost you something you can't
get back by trying again. That's the actual test to apply when you're
deciding whether some new action your agent wants to take belongs on
this list: if I re-ran the job right now, would that undo the damage? If
no, it needs a human gate, unconditionally.

### Slide 24 — Sandboxing: Limiting the Blast Radius

Permission scoping tells the agent what it's *allowed* to ask for.
Sandboxing is the second, independent layer — it limits the damage *if*
that permission boundary turns out to be misconfigured, because let's be
honest, permission configuration is exactly the kind of thing that gets
misconfigured.

Three concrete practices: run in an ephemeral CI runner or container that
gets destroyed the moment the job ends — no state persists for an
attacker, or a bug, to exploit later. Use a service account scoped to
this one repository, not an org-wide credential — so a compromised job
in Repo A can't touch Repo B. And simplest but most-skipped: don't put
production credentials in the job's environment at all, if the job
doesn't need them. Not "restrict access to them" — don't put them there.
An agent can't leak, misuse, or accidentally exfiltrate a credential that
was never present in its environment to begin with.

Look at the YAML snippet — this is the GitHub Actions `permissions` block
at the job or workflow level. `contents: write` scoped to this repo,
`pull-requests: write` for opening the auto-fix or changelog PR — and the
comment matters: if the job never touches issues, don't include `issues:
write` even set to some restrictive value; omit the key entirely. Default
GitHub Actions permissions are more generous than most jobs need, and
"I'll just leave the default" is exactly the kind of decision that turns
into next quarter's security incident.

---

## Human-in-the-Loop Gates (Slides 25–31) — ~15 min

### Slide 25 — Designing the Gate: No Human Watching Live

We've spent three sections on "what should the agent never do" and "how
do we contain it if it tries anyway." Now the constructive half: how do
you actually get a valid approval when there's no person standing by,
watching the pipeline execute, ready to click a button at the right
moment?

The answer is that "approval" has to become a structural property of the
system, not an event a person performs live. Three patterns that work in
practice, and I want you to notice what they have in common: required PR
review — the agent opens the PR, sure, that's fine, but merging requires
either a specific human approval or a review policy your team already
trusts, like one required approval plus CODEOWNERS coverage. Draft-only
output — the artifact the agent produces is *inert* by default; a
release stays a draft, a PR stays unmerged, a changelog stays unsent,
until a human actively promotes it to its "live" state. And branch
protection — configuring `main` itself to require status checks and
review before anything lands there, so that even if an agent's identity
were fully compromised, it structurally cannot merge around the
protection.

What all three have in common: the check happens automatically, at a
point in the system that doesn't depend on anyone being present at the
exact moment the agent finished its work. That's the whole trick. You're
not simulating a human watching — you're replacing "a human watches" with
"the system refuses to proceed without a specific, checkable condition
being true."

### Slide 26 — Gate Example: Branch Protection + Required Review

Let's make that concrete. This is illustrative configuration — I want to
be upfront that this isn't a YAML file you literally paste somewhere;
it's a stand-in for settings you'd configure through your Git host's
branch protection UI or API, whether that's GitHub, GitLab, or something
else. But the shape of it is exactly right: `main` requires at least one
approving review, requires that a code owner specifically be among the
approvers if `CODEOWNERS` applies to the changed files, restricts direct
pushes entirely — meaning even a maintainer, even the agent's own
service account, cannot push straight to `main` — and requires the
`lint` and `tests` status checks to pass.

Here's the line I want you to remember, because it's the thesis of this
entire slide: the gate lives in repo config, not in the agent's prompt.
If your only safeguard is a sentence in a system prompt saying "ask
before merging," that's a *suggestion* — a well-behaved model will
usually follow it, an unusual context, a subtly ambiguous instruction, a
future model version with different tendencies, any of these could break
it, and you'd have no way of knowing until it already happened. Branch
protection configured at the repo level is a wall. It doesn't care what
the agent "intends" to do. It mechanically blocks the merge until the
condition is satisfied. That difference — suggestion versus wall — is
the entire reason this module exists.

### Slide 27 — Anti-Patterns to Avoid

Let's close this section with four ways teams get this wrong in
practice, because I promise you, you will see at least one of these in
the wild within your first year of working with agent-driven pipelines.

The agent reviewing its own PR — same identity opens it and approves it.
Sounds absurd stated baldly, but it happens by accident constantly: a bot
account has both "create PR" and "approve PR" scopes because nobody
thought to separate them, and now your required-review gate is
satisfied by the same actor that made the change. It's a gate in name
only.

Broad token, narrow prompt — the classic mismatch. The system prompt
says "don't force-push," but the credential backing the agent's git
access technically *can* force-push. The rule lives in the wrong place —
in language the model interprets, rather than in a permission the
credential simply doesn't have. Fix this by removing the *capability*,
not by writing a more emphatic sentence.

Silent auto-merge — any pipeline where "the tests passed" is sufficient
on its own to merge to `main`, with no review step in between, has
quietly deleted the gate you thought you designed. This creeps in
gradually — someone adds `auto-merge` to speed up a backlog of trivial
PRs, and six months later nobody remembers that the agent's lint-fix PRs
are matching that same auto-merge rule.

One shared bot credential for everything — the convenience trap. It's
much easier to set up one service account and reuse it for lint-fix,
triage, and release drafting than three separately scoped ones. But now
a single compromised credential has the union of every permission any of
those three jobs ever needed, which is a much bigger blast radius than
any one job justified on its own.

---

### Slide 28 — Patterns That Work Instead of Anti-Patterns

Anti-patterns are easy to remember as "don't do this", but it's more
useful to know what to do instead. Walk the table row by row. Agent
reviews its own PR — create a separate identity for the reviewer with
read and comment rights only, and leave approval to a human or
`CODEOWNERS`. Broad token — issue a per-job token with `permissions:`
exactly for the task.

Silent auto-merge isn't necessarily evil: for a narrow low-risk class,
say patch dependency bumps with a full test suite, it's acceptable, but
through a merge queue and required checks. Split the shared token into
bots by role. Replace "ask before merge" in the prompt with branch
protection. And last: protect the agent's own hooks and CI configs from
it, or it can lift the restrictions itself.

### Slide 29 — An Agent-Only System: Architecture

How to build a system where only agents execute. The scheme is a
pipeline. An issue reaches the Planner: it reads the repo and writes a
plan into the issue. The Implementer writes code only to its own branch
and opens a PR. Next it isn't an agent but ordinary CI gates: tests,
linters, scanners. Then the Reviewer — another agent, another identity,
read and comment only. And the merge queue merges only if checks are
green and policy is satisfied.

The key idea is alternation. Agents don't check each other directly:
between them stand deterministic gates that can't be "persuaded". If a
gate is red or the reviewer disagrees, we send it back to the
Implementer, but with an iteration limit; limit exhausted — escalate to
a human. The human in such a system doesn't execute but owns the
policy: writes the boundaries, samples results, handles escalations.

### Slide 30 — Rules for a System of Agents

Four design rules. First — roles differ in identity and permissions:
whoever writes cannot approve. Second — communicate through artifacts.
Don't shuttle a huge shared context from agent to agent: let one leave a
plan in the issue and another read it. Then state lives in git, a human
can see it, it can be resumed after a failure and rolled back.

Third — deterministic gates stand between agents. If a model checks a
model, their blind spots may coincide. Tests and scanners don't share a
model's blind spots. Fourth — idempotency: CI may start the agent twice,
and the second run must not open a second identical PR. Look for an
existing one first, then create.

### Slide 31 — Safety Limits, Observability, and the Human's Place

A system of agents without safety limits is a generator of bills and
incidents. Budgets: a ceiling on steps, time, the number of "fix —
verify" iterations — three attempts and enough — and a cost ceiling per
job and per day. Kill switch: one variable that turns off all agents;
the main thing is to check at least once that it works.

Observability: without logs you won't understand what the agent did.
Keep the hook and action logs, count the revert rate, the escalation
rate and the price of one PR — these are your instruments. And
escalation: an agent that is unsure or hit a limit must call a human,
not guess.

The last point matters. "Agents only" means "no human in the execution
loop", not "nobody accountable". A human owns policy and audit;
otherwise nobody bears responsibility and nobody improves the
boundaries.

---

## Lab and Deliverable (Slides 32–33) — ~10 min intro, remainder hands-on

### Slide 32 — Lab: Wire an Agent into a Pipeline

Here's today's hands-on work. Pick one of two options — don't do both,
depth beats breadth here. Option one: wire up lint auto-fix on PR open,
committing to the PR's own branch, with human review required before
merge — essentially building out Pattern 1 from Slide 19 for real, in
your own sample repo. Option two: draft a `CHANGELOG.md` entry from the
commits since the last tag, opened as a PR, and — this is the part
people skip if you don't say it out loud — never auto-merged under any
condition.

Two hard requirements regardless of which you pick. First, a working
config — an actual CI workflow file, or a git hook plus its backing
script, something that runs, not just something described in prose.
Second — and this is the part of the lab that's actually being graded,
so to speak — a concrete, explicit approval gate sitting before anything
destructive or externally visible happens. If your config technically
works but a bad output could reach `main` or leave your infrastructure
without a human in the loop, the lab isn't done, no matter how well the
happy path performs.

Go build this now against the shared sample repo. Budget real time for
it — this is exactly the kind of task that looks like fifteen minutes of
YAML and turns into forty-five minutes once you actually try to get the
permissions and the gate right.

### Slide 33 — Deliverable

When you're done, you're handing in two things. First, obviously, the
working pipeline config itself — the workflow file or hook script you
just built. Second, and don't shortchange this part: a short written note
listing exactly what this automation is *not* allowed to do unattended,
and why each of those boundaries exists.

Don't write vague boundaries — tie each one back to something specific.
Either it maps directly onto the never-list from Slide 23 — "this can't
force-push because history rewrites aren't undoable by re-running" — or
it's a risk specific to your project that you identified yourself, which
is honestly the more interesting kind of answer, because it shows you
internalized the *reasoning*, not just the list. If your note reads like
you copy-pasted the four bullets from Slide 23 with no connection to your
actual pipeline, that's a sign you haven't actually thought through what
your specific automation could do wrong.

---

## Recap & Next Module (Slide 34) — ~5 min

### Slide 34 — Recap & Next Module

Let's land the plane. Three things to leave with today.

One: unattended agents need boundaries designed in ahead of time, never
assumed after the fact. Hooks, permission scopes, and sandboxes are the
mechanisms that make that concrete — not vibes, not a well-written
prompt, actual enforced structure.

Two — and this is the phrase I want stuck in your head walking out of
here — draft, don't send; propose, don't merge. Structural gates beat
prompt instructions every single time, because a structural gate doesn't
care how persuasive the context around it was.

Three: the never-list — force-push, delete, send, spend — applies
regardless of how convenient it would be to skip it in some particular
case. "Just this once, it would save so much time" is exactly the
reasoning that precedes the incident report.

Where we go next: Module 14 is Governance, Safety, and Team Adoption.
Today was about designing guardrails for one pipeline, one repo, largely
as an individual decision you make when you wire something up. Module 14
is about what happens when this needs to scale to an entire team or
organization — turning the judgment calls you made today into written
norms other people can follow without having sat through this lecture.
See you there.
