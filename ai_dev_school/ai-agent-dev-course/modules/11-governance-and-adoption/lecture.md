# Module 11 — Lecture Script: Governance, Safety & Team Adoption

This is the full spoken script for a live session, slide by slide, matching
`slides.md`. Timing notes are cumulative suggestions for a ~2–2.5 hour
session including the hands-on lab; adjust to your room's pace.

---

## Slide 1 — Module 11: Governance, Safety & Team Adoption

*(~5 min — cold open)*

Welcome back. If you've been with us since Module 1, you've now got five
different ways to direct an agent on a task — document-driven development,
plan-first workflows, TDD-with-agents, conversational iteration, and
multi-agent review. You've felt the tradeoffs directly, because you built
the same kind of feature five different ways.

Today we're not adding a sixth methodology. Today we're stepping back and
asking a completely different question: who decides which one to use, and
how does a whole team — not just you, sitting at your desk — make that
decision consistently, safely, and in a way that survives someone new
joining six months from now?

This module is titled "Governance, Safety & Team Adoption," and I want to
be upfront that "governance" is a word that makes a lot of engineers
nervous — it sounds like process for its own sake, like something a
compliance team invents to slow you down. That is not what we're building
today. What we're building is closer to a style guide, or a linter config,
for *how your team decides how to work with agents*. It's the difference
between every developer relitigating the same question on every single
PR — "should I have used a spec for this?" — and having that question
answered once, in a document, so people can spend their judgment on the
genuinely hard edge cases instead.

By the end of today you'll have a real artifact: a one-page policy your
own team could actually adopt on Monday.

---

## Slide 2 — Agenda

*(~2 min)*

Here's the shape of the next couple of hours. We'll start with disclosure
— does a PR need to say it was agent-assisted, and does anyone care. Then
review requirements tied to risk, not vibes. Then the centerpiece: a
decision framework that takes a task description in and hands you a
methodology out, built directly from the comparison matrix in the
syllabus appendix — the one you've seen referenced since Module 3 and
finally get to use in full. Then metrics — what to actually measure, and
the trap most teams fall into when they only look at speed. Then three
failure modes I guarantee you've either seen or will see. And then the
lab, where you build your own version of all of this for a team you
choose — real or hypothetical.

---

## Slide 3 — Objectives

*(~3 min)*

Five concrete things you should be able to do walking out of here. Draft
a disclosure norm — one or two sentences, not a policy novel. Set review
requirements that key off risk tier, so you're not deciding review
rigor PR by PR out of gut feel. Build an actual decision tree, task type
in, methodology out. Pick metrics that would actually catch it if agent
use were quietly making things worse while looking faster. And recognize
the three failure modes we'll cover before your team falls into them,
not after.

Notice none of these are "learn a sixth methodology." Everything today
is about the layer *above* methodology choice — the policy layer.

---

## Slide 4 — From Individual Habit to Team Policy

*(~10 min)*

Let's ground this in why it matters. In Modules 3 through 9 you built
judgment. You now have a feel for "this is ambiguous enough to need a
spec" or "this is a quick prototype, just talk to the agent." That
judgment is genuinely valuable and I'm not asking you to throw it away.

But here's the problem the moment you're not the only person on the
team. Say you're reviewing a PR. Before you even open the diff, you need
to know: what bar am I applying here? Is this the kind of change where I
should be reading every line like it's going into a pacemaker, or is
this a Tuesday-afternoon internal tool where "looks reasonable, tests
pass" is a fine bar? If that answer lives only in the head of whoever
wrote the PR, you as the reviewer are flying blind. You might apply too
light a touch to something that actually mattered, or burn an hour
carefully reviewing a throwaway script.

Now scale that to a new hire. They join, they've never taken this
course, they've never seen your team argue about this in Slack six
months ago. What do they do by default? If the answer is "ask around and
absorb the culture," you have not built a policy, you've built a
folklore, and folklore does not scale and does not survive turnover.

And here's the phrase I want you to actually distrust when you hear it
in a retro: "it depends." It depends is true! Almost everything depends.
But "it depends" is not, by itself, actionable. The job of governance is
to answer *on what* it depends, and to write that down as a small number
of concrete questions — which is exactly what we're building today.

One more framing before we move on, because I don't want this to sound
like I'm asking you to become bureaucrats: the goal isn't to remove
judgment from the system. It's to make the *default* explicit, so that
judgment — the expensive, scarce resource — gets spent on the actual
hard edge cases, the ones that don't fit the tree cleanly, instead of
being re-spent every single day on questions that already have a good
answer.

---

## Slide 5 — Disclosure Norms — The Core Question

*(~8 min)*

First concrete piece of policy: disclosure. Does a pull request need to
say, somewhere, "this was built with an agent"?

I want to walk you through both ways this goes wrong, because both are
common, and they're opposite failures.

Failure one: no disclosure at all, ever, by convention or by omission.
What happens is subtle. A reviewer looks at a diff. They don't know an
agent produced most of it. So they apply the same mental model they'd
apply to a human-written PR — which includes assumptions like "the
author probably only touched what they needed to" or "if there's an
unusual pattern here, the author probably had a specific reason." Those
assumptions are often *wrong* for agent output, in ways that are
specifically agent-shaped — silent scope creep, a plausible-looking but
subtly wrong API call, a refactor that touched twelve files when three
would do. A reviewer who doesn't know to look for those things won't go
looking for them. Non-disclosure doesn't just hide information, it
actively steers the reviewer's attention in the wrong direction.

Failure two, and this one surprises people: disclosure that changes
nothing. Team adds a PR label, "ai-assisted." Everyone dutifully checks
the box. And then... nothing happens differently. No different review
process, no different bar, nothing. At that point the label is pure
decoration. It creates the appearance of governance — "look, we track
this!" — with none of the substance. Worse, it can create false comfort:
leadership sees the label being used and assumes there's a policy behind
it, when there isn't one.

So the real question was never "disclose, yes or no." The real question
is: **what changes once we know?** If you can't answer that, don't
bother with the label yet — go figure out the "what changes" part first,
which is exactly what the next two slides and the risk-tier table are
for.

---

## Slide 6 — Disclosure Norms — What a Working One Looks Like

*(~8 min)*

So what makes a disclosure norm actually work? Two properties: it has to
be *checkable*, and it has to be *consequential*.

Checkable means it's not "use your judgment about whether to mention
it." It's a specific, low-friction, hard-to-forget mechanism. A checkbox
in the PR template. A commit trailer — you've all seen `Co-authored-by:`
trailers in git history; the same pattern works fine here, something
like `Assisted-By: Claude Code`. Or a required label that CI actually
checks for before allowing merge. The point is it should take the author
five seconds and it should be something a bot could audit later if you
needed to.

Consequential means disclosure actually *triggers* something. A few
options, and pick what fits your team: touching a high-risk path
(which we'll define on the risk-tier slide) plus the disclosure flag
together requires pulling in an extra reviewer. Or: disclosed
agent-assisted PRs don't get the fast-track review SLA that a trivial
human PR might get — because "trivial-looking" and "actually trivial"
are not the same thing when an agent wrote it. Or, and I like this one a
lot for encouraging good practice rather than punishing agent use: the
PR description is required to name which methodology was used — "this
was DDD against spec X" or "this was conversational, no spec." That
single sentence does double duty — it's disclosure, and it tells the
reviewer which of today's five review postures to adopt.

I want to leave you with one somewhat sharp framing here, because I
think it changes how people internalize this: undisclosed agent-assisted
work that gets *discovered* later — say, in an incident postmortem, or
because someone recognized the style — is a bigger trust problem for
your team than almost anything that could be wrong with the code itself.
Bad code gets fixed. A team that learns it can't trust what people tell
it about how work got done has a much deeper problem. So when you write
your policy in the lab, treat non-disclosure itself, not just bad code,
as the thing worth having a consequence for.

---

## Slide 7 — Review Requirements by Risk Tier — Concept

*(~6 min)*

Let's move to review requirements. The core idea here is simple, and
honestly it's not new — it predates agents entirely. Not all code has
the same blast radius when something goes wrong. A one-line copy change
on a marketing page and a change to how you compute a billing invoice
are not the same kind of risk, and your team probably already reviews
them differently without ever having written that down.

What agents change is not the *principle* — it's the temptation to skip
the principle. Here's why: agent output tends to look clean. Well-
formatted, consistent style, sensible variable names, maybe even a nice
commit message. A rushed, risky diff from a stressed human at 6pm on a
Friday often *looks* rushed — inconsistent formatting, a rambling commit
message, obvious signs of "I just want this merged." An equally risky
diff from an agent can look calm, polished, and confidence-inspiring,
even when it's just as dangerous. Clean-looking is not the same as
low-risk, and that gap is exactly where teams get burned. So we tie the
review bar to what the change *touches*, mechanically, not to how
composed the diff looks.

---

## Slide 8 — Risk Tiers — A Starting Table

*(~10 min)*

Here's a starting table — three tiers, high, medium, low. I want to be
clear this is a template, not gospel. The specific paths will differ for
every team; what should transfer is the *shape*: risk tier maps to a
floor methodology and a review bar.

High risk: authentication, billing, data migrations, permissions —
anything where a mistake is either hard to reverse or actively harmful to
users or the business if it goes wrong silently. For this tier, the
floor is DDD or TDD plus a multi-agent reviewer pass from Module 8, and
critically, human sign-off is required — an agent reviewer catching
issues doesn't substitute for a human saying "yes, ship it," it's an
additional filter before the human even looks. Review bar: two human
reviewers, and nobody merges their own high-risk PR even if they have
the permissions to.

Medium risk: shared libraries, public APIs, anything that crosses team
boundaries — code where the blast radius is real but more contained,
and where the main danger is surprising someone else's team rather than
an outage. Floor methodology is DDD or plan-first — you want *some*
durable artifact, spec or plan, that the other team can look at without
reverse-engineering intent from the diff. One human reviewer, and the
spec or plan gets attached to the PR, not just described in the
description box.

Low risk: internal tooling, prototypes, scripts with a single owner —
things where if it's wrong, the blast radius is "this internal script
does the wrong thing and the owner notices and fixes it." Conversational
mode is completely fine here. One reviewer, asynchronous review is fine,
nobody needs to drop what they're doing.

Take this table home and rewrite the middle two columns for your actual
repo structure. The paths that are "high risk" for a fintech company
and for an internal dev-tools team look completely different. What
should not change is that you *have* three tiers and that each one has
an explicit floor and an explicit bar, written down, not implied.

---

## Slide 9 — A Decision Framework: Task Type → Methodology

*(~7 min)*

Now, risk tier answers the reviewer's question: how carefully do I need
to look at this. But the author has a different, earlier question:
before I even start, what kind of task is this, and which methodology
fits it?

These are genuinely different axes, and it's worth spending a minute
making sure that lands, because it's the single most common confusion
people have when they first try to build one of these frameworks. A CSS
tweak to your login page is extremely *visible* — everyone sees the
login page — but it's not ambiguous. There's a clear, narrow, verifiable
change. Conversely, a brand-new internal batch job that processes some
data nobody outside the data team will ever look at is low-risk by our
tier definition, but might be *highly* ambiguous — nobody's fully
specified what "correct" output looks like yet.

So: task type picks the methodology — what's the best way to direct the
agent given the nature of the work. Risk tier picks the review bar on
top of whatever methodology got picked. They compose. A task can be
"ambiguous and high-risk" — that's DDD *and* the two-reviewer bar. Or
"ambiguous and low-risk" — DDD, but one async reviewer is fine. Keep
these two axes separate in your head and in your policy document; if
you conflate them you end up with a much messier tree that tries to
answer two questions with one branch.

---

## Slide 10 — The Methodology Comparison Matrix

*(~8 min)*

This is the table you've been promised since Module 3 — straight from
the syllabus appendix, and it's the raw material for everything we do
for the rest of this session, so let's actually walk it row by row.

DDD, spec-first: best for features with real ambiguity, or where
multiple people need shared context on intent — because the spec *is*
the shared context. Weak for tiny fixes, where writing a spec is pure
overhead relative to the size of the change. What it leaves behind: a
durable spec doc — something that outlives the PR.

Plan-first: best for refactors and risky multi-file changes, where you
want agreement on the *approach* before anyone touches code. Weak for
fast exploration — if you don't know what you want yet, writing a plan
first just means writing a plan you'll immediately discard. Leaves
behind an ephemeral plan, or if the decision's worth keeping, an ADR.

TDD-with-agent: best for bug fixes and well-defined logic — anywhere you
can write down "this input should produce this output" before you start.
Weak for vague or exploratory UI work, where you don't yet know what
"correct" even looks like, so you can't write the test first. Leaves
behind a test suite — arguably the best artifact of the five, because it
keeps paying off.

Conversational: best for prototypes, one-off scripts, pure exploration.
Weak for anything that needs a paper trail — by design, there isn't
one, just chat history that nobody's going to read again. Leaves behind
nothing durable.

Multi-agent review: best for high-stakes, security-sensitive changes,
where you want a second set of eyes — agent or human — before it ships.
Weak for low-stakes or small changes, where the coordination overhead of
running a whole review pipeline swamps the size of the change itself.
Leaves behind a review transcript.

Notice the pattern across all five: the "best for" and "weak for"
columns are mirror images of each other, and the artifact column tracks
how much durability the situation actually needs. That's not a
coincidence — it's the whole design principle behind the decision tree
we're about to build.

---

## Slide 11 — Turning the Matrix into a Decision Tree

*(~10 min)*

Here's how we turn that table into something someone can actually run
in thirty seconds without re-deriving it from first principles each
time. It's a small tree, about five questions, and I want to walk
through *why* it's ordered this way, not just what it says, because the
order matters.

First question, and it comes first on purpose: does the task touch a
high-risk path? This is checked before anything else because risk tier
is a *gate*, not just another branch — if the answer is yes, you're
already at DDD or TDD plus multi-agent review plus human sign-off,
full stop, regardless of how the rest of the tree would have answered.
Risk overrides convenience every time.

If no — now we're in "pick the right-fit methodology" territory, and we
walk the matrix's own logic. Is the requirement genuinely ambiguous, or
does it need shared context across multiple people? That's DDD's sweet
spot — spec first. If not, is it a refactor or a structural, multi-file
change? That's plan-first's sweet spot — agree on the approach before
touching code. If not, is it a bug fix with a reproducible failure you
could write a test for? That's TDD-with-agent. And if none of the above
— it's not risky, not ambiguous, not structural, not a reproducible bug
— you've landed on conversational, which is exactly right, because
that's the profile of a prototype or a one-off.

Notice what's *not* on this tree: multi-agent review as a standalone
branch anywhere except the risk gate at the top. That's deliberate —
in the comparison matrix, multi-agent review is best for high-stakes
work, which is exactly what the risk gate already catches. You don't
need a separate branch for it because risk tier already routes you
there.

I'll say the obvious thing explicitly: this exact tree is a starting
point, not the answer key. Your team's actual task types might need a
different third or fourth question. What you're borrowing from this
slide is the *pattern* — risk gate first, then task-shape questions in
order from "most work saved by getting it right" to "least" — not the
literal five questions.

---

## Slide 12 — Decision Tree — Walked Through Twice

*(~8 min)*

Let's run two real task descriptions through it so you can see it in
motion before you build your own.

Task A: "Add a retry with backoff to the billing webhook handler." First
question — does it touch a high-risk path? Billing — yes, immediately.
We don't even need to ask if it's ambiguous or a refactor or a bug fix,
because the gate already fired. Answer: DDD or TDD, plus multi-agent
review, plus required human sign-off, two reviewers, no self-merge. Even
if this is a three-line change and feels like it should be quick, the
tree doesn't care how small the diff looks — it cares what it touches.

Task B: "Try three different empty-state illustrations on the onboarding
screen, we'll pick one." High-risk path? No — onboarding illustrations,
nobody's balance is at stake. Genuinely ambiguous requirement needing
shared context? Not really — "try three, we'll pick" is about as
self-contained as a task gets. Refactor or structural multi-file
change? No. Reproducible bug with a test you could write? No, there's no
bug here at all. So by elimination: conversational. Fastest path, and
correctly so — writing a spec for "try three illustrations" would be
pure theater.

What I want you to take from these two examples isn't the specific
answers — it's that the *same five questions*, asked in the *same
order*, produced two completely different, and both completely correct,
defaults. That consistency, not the specific outcome, is what a decision
tree is actually buying you.

---

## Slide 13 — Metrics That Matter

*(~8 min)*

Let's shift from "how do we decide" to "how do we know if any of this is
actually working." Three signals, and I want to stress up front: track
all three, always split by agent-assisted versus human-only, side by
side, same time period, same team.

Cycle time — the duration from opening a PR to it actually merging. This
is the metric everyone reaches for first because it's easy to pull and
agents are, unsurprisingly, often genuinely fast at producing a first
draft.

Revert or rollback rate — how often a merged change later gets undone,
either a git revert or a hotfix that effectively undoes the behavior.
This is your quality signal, and it's lagging — it shows up weeks after
the PR merged, which is exactly why teams under-weight it in the moment.

Review comment volume — how much reviewers actually had substantive
things to say. Counterintuitively, this can go *down* in an unhealthy
way, not just a healthy one — more on that in a second.

The instruction here is simple but the discipline is hard: don't look
at any one of these alone. Cycle time alone tells you agents are fast,
which you already knew. Revert rate alone, without a cycle-time
baseline, doesn't tell you if the tradeoff is worth it. It's the
*combination* that tells you something you didn't already know.

---

## Slide 14 — The Speed Trap

*(~10 min)*

Now the trap, and I want to describe it as a story because that's how it
actually happens on real teams. A team adopts agent-assisted
development. Cycle time drops — maybe 30%, maybe 50%, genuinely
impressive. Leadership is thrilled. It goes in the quarterly update.
Everyone feels good. Nobody looks any further, because why would you —
the number you were told to watch went the right direction.

Three months later, someone happens to pull revert rates for an
unrelated reason — maybe an incident review — and notices agent-assisted
PRs are reverting or getting hotfixed two to three times as often as
human-only PRs from the same period. And here's the detail that makes
it worse, not better: review comment volume *per PR* has also quietly
fallen over that same window. That's not because the code got better —
it's because reviewers, faced with more PRs arriving faster, and PRs
that *look* clean, started skimming instead of reading closely. The
review bar existed on paper. It eroded in practice, silently, and
nobody noticed because nobody was tracking review depth as a number —
they were tracking merge speed.

Here's the one-liner I want you to remember: faster, plus more reverts,//
is not actually faster — once you count the cost of the revert, the
incident response, the re-review of the fix, the trust cost with
whoever got paged — the *net* time to a durably-shipped feature might be
worse than before you adopted agents at all. Cycle time measures time to
merge. It does not measure time to *actually done*.

And here's the sharpest version of the point: a dashboard with only
cycle time on it is worse than no dashboard at all. No dashboard, at
least, leaves people uncertain and maybe a little suspicious. A
dashboard with a reassuring, incomplete number gives people *false*
confidence, stated with the authority of a chart. If you only ever
measure the thing agents are obviously already good at — raw speed —
the only thing you will ever learn is that agents are fast. You already
knew that on day one.

---

## Slide 15 — A Minimal Metrics Review

*(~6 min)*

So what's the actual practice, not just the warning? Pull these three
numbers monthly — doesn't need to be more often than that for most
teams, this isn't a daily standup metric — split by agent-assisted
versus human-only.

Then look for the pattern that actually matters, not just the raw
numbers: cycle time down *and* revert rate flat or down — that's a real
win, keep going, maybe even loosen the policy a little where it's overly
cautious. Cycle time down *and* revert rate up — that's the speed trap
showing up in your own data, and the correct response isn't panic or a
ban on agents, it's to tighten something specific: raise the review bar
on the tier where reverts are concentrated, or move a task type up to a
stricter floor methodology in your tree.

I want to be explicit that this isn't a "gotcha, agents bad" slide. This
is a feedback loop. The whole point of measuring is that it lets you
*adjust the policy* based on evidence from your own team, instead of
either blind faith or blind suspicion. Most teams that do this loop find
some tasks where agents are a clear net win and some where the current
floor methodology is too loose — and they adjust the tree, not their
overall stance on agents.

---

## Slide 16 — Failure Mode 1 — Methodology by Habit

*(~7 min)*

Let's get concrete about three failure modes I'd bet money you'll
recognize, or will see within a year of your team adopting agents
seriously.

First: methodology by habit. Here's the pattern. A developer has one
great experience with conversational mode — quick, fun, low-friction,
worked great on a prototype. So they keep reaching for it. For
everything. Including, eventually, the change to the authentication
flow, which absolutely needed DDD and a risk-tier-appropriate review,
and got neither, because the developer's default tool was conversational
and nobody stopped them.

The tell, if you're watching for it, is a specific and slightly
uncomfortable correlation: the methodology used on a PR correlates with
*who wrote it*, not *what it touches*. If you can predict someone's
methodology choice from their name better than from the task
description, you have this failure mode, whether or not anyone's
noticed yet.

The fix is exactly the decision tree from Slide 11 — and notice this is
the *first* practical payoff of building one. It's not primarily a
documentation exercise. It removes the choice from personal preference
entirely. The task type and risk tier decide. The author doesn't get to
default to their favorite mode, because there's no "default mode" left
to default to — there's a tree.

---

## Slide 17 — Failure Mode 2 — Specs Written and Never Updated

*(~7 min)*

Second failure mode, and this one's sneakier because it looks like doing
the right thing initially. A team does DDD properly — writes a real
spec, hands it to the agent. But implementation always surfaces things
the spec didn't anticipate, that's normal, that's what Module 3 called
the spec-update loop. The problem is when that loop breaks: the
implementation drifts from the spec during the work, and *nobody goes
back and updates the document*.

Now you have a spec doc sitting in your repo that describes a system
that doesn't quite exist anymore. And here's why this is actually worse
than never having written a spec at all: a stale spec doesn't look
stale. It looks exactly as authoritative as a current one — same
formatting, same location, same "official-looking" header. The next
engineer, or the next agent session, reads it and trusts it, and now
they're building on a foundation that's subtly wrong in ways that are
hard to detect until something breaks.

The fix has to be structural, not aspirational — "please remember to
update the spec" doesn't survive contact with a deadline. Make the
spec-update loop a policy requirement with an actual checkpoint: the PR
template asks, as a required field, not optional, "does the spec still
match what's implemented? If not, what changed and did you update it?"
That question costs the author thirty seconds and it's the difference
between a spec that stays trustworthy and one that quietly rots.

---

## Slide 18 — Failure Mode 3 — Review Fatigue

*(~7 min)*

Third failure mode, and this is the one that connects most directly back
to the speed trap from Slide 14. Agents can produce diffs that *look*
review-ready — clean formatting, plausible structure — much faster than
a human review cadence was ever designed to absorb. Your review process
was calibrated for a world where PRs arrive at human-typing speed.
That assumption just broke.

What happens next, if nobody intervenes, is entirely predictable:
reviewers, faced with a growing queue of clean-looking diffs, start
rubber-stamping. Not out of laziness — out of simple bandwidth. The
review requirement still exists in your policy document. It has quietly
stopped existing in practice. This is exactly the mechanism behind that
"review comment volume falling" data point from the speed trap slide —
now you know *why* it falls, not just that it does.

Two concrete fixes, pick one or both. Cap agent-assisted PRs per
reviewer per day — a hard ceiling that forces load-balancing instead of
letting the queue back up onto one exhausted person. Or, and I think
this is the more elegant fix: require the multi-agent reviewer pass from
Module 8 to run automatically *before* a human ever opens the diff, so
what lands in the human queue is already pre-filtered — obvious issues
caught, only the PRs that need real human judgment actually reach a
human. Either way, the goal is the same: match the review bar to what a
human can actually sustain, not to what looks good in the policy
document.

---

## Slide 19 — Anatomy of a Team Policy Doc

*(~6 min)*

We've now covered all four pieces. Let's assemble them into the actual
artifact — the thing you'll build in the lab and the thing your team
would actually adopt.

Five sections, one page. Disclosure norm — how a PR states it was
agent-assisted, and critically, what that disclosure *triggers*, per
Slide 6. Decision tree — task description goes in, methodology comes
out, per Slide 11. Review requirements per risk tier — the table
structure from Slide 8, filled in with your team's actual paths.
Metrics — what's tracked, how often, and what specific finding would
trigger a policy review, per Slides 13 through 15. And known failure
modes, named explicitly — not because naming them prevents them by
magic, but because a team that has a name for "methodology by habit"
can say that phrase out loud in a retro and everyone knows exactly what
they mean, which is half the battle.

One more thing on format, and I mean this literally, not as a
soft suggestion: one page. If your policy document is four pages, it
will get skimmed once at onboarding and never opened again. If it's one
page, someone can pin it, print it, keep it open in a tab. Length is not
a proxy for thoroughness here — it's the opposite. The discipline of
fitting this on one page is itself valuable, because it forces you to
cut the caveats and edge-case discussions down to the tree and the
table, and put the nuance in a separate doc if you truly need it.

---

## Slide 20 — Lab — Build Your Team Policy + Decision Tree

*(~5 min intro, then hands-on — reserve 45–75 min of session time)*

Here's the lab. Pick a team — your real one, or a hypothetical one if
that's easier to reason about cleanly. Five steps.

Start from the comparison matrix on Slide 10 — that's your raw material,
don't skip re-reading it. Build your decision tree — and I want to
stress, Slide 11 is a *template* for the pattern, not an answer you copy
verbatim. Adapt the actual questions to your team's real task types; if
your team does a lot of data-pipeline work, "is this a reproducible bug"
might need to become two questions, not one. Define your own risk tiers
and fill in the review bar at each — don't just reuse my example paths,
write down the ones that are actually true for your codebase. Write one
disclosure norm sentence, and hold yourself to the two-property test
from Slide 6: is it checkable, and is it consequential? If you can't
answer both yes, revise it before moving on. And finally — this step is
not optional, it's the actual test of whether your tree works — take
three real, recent task descriptions from your own backlog or history
and run them through your own tree. Do the outputs feel right? If a task
you know should have needed careful review comes out the other end as
"conversational, ship it," your tree has a bug, and it's much better to
find that now than in production.

I'll circulate while you work — flag me if your tree keeps producing
answers that feel wrong; that usually means a question is in the wrong
order, not that the whole approach is broken.

---

## Slide 21 — Deliverable

*(~3 min)*

To be explicit about what you're handing in: one page, containing the
decision tree, the review requirements by risk tier, and the disclosure
norm. That's the team policy doc.

The bar I want you to hold yourself to while you write it — and this is
also how I'd suggest you self-grade it — is the one from the syllabus:
could a brand-new team member follow this document *without having
taken this course*? Not "would they understand the philosophy behind
it" — could they mechanically follow it: read a task description, get a
methodology, know what review bar applies, know how to disclose. If your
document requires the reader to already know what DDD or plan-first mean
in detail, either link back to those definitions briefly or your policy
doc has failed its own test.

---

## Slide 22 — Recap & Next Module

*(~5 min)*

Let's close the loop on today. Governance, at its core, is what turns
individual judgment into a team default — not to eliminate judgment, but
so it gets spent on genuine edge cases instead of being re-litigated on
every single PR. We tie review rigor to risk tier, because blast radius
is what actually matters, not how the diff looks. We tie methodology to
task type, using the comparison matrix as the source of truth. We
disclose in a way that's both checkable and consequential, or we don't
bother. And we measure cycle time, revert rate, and review volume
*together*, because any one of them alone will only ever tell you the
flattering half of the story.

That's the whole course's worth of methodology, now wrapped in a layer
that lets a team actually run it, not just an individual.

Next time is the Capstone — Module 12. This is where everything comes
together on one real feature: you'll deliberately combine
methodologies — DDD for the spec, plan-first for the approach, TDD for
the core logic, a reviewer agent before merge — the way a mature team
guided by exactly the kind of policy you just wrote would actually work.
Bring the policy doc you built today; you'll want it.
