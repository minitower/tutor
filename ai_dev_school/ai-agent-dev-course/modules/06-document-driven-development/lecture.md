# Module 6 — Lecture Script: Document-Driven Development (DDD)

*Speaker notes for the instructor. Matches `slides.md` slide-for-slide (21 slides). Read the bracketed timing notes as a pacing guide, not a stopwatch — adjust to the room.*

---

## Slide 1 — Module 6 / Document-Driven Development (DDD)

**[~2 min]**

Welcome back. This is Module 6, and the title is Document-Driven Development — DDD for short. Don't confuse it with Domain-Driven Design, which is a different DDD from a different decade; if anyone in the room has that acronym loaded already, tell them to set it aside for the next two hours.

Here's the one-sentence version of what we're about to spend two hours on: when you're working with a coding agent, a written spec is the thing you should be handing it — not a paragraph in chat, not a verbal explanation, not "you know what I mean." The case study running through this whole module is a spec document functioning as the source of truth between you and the agent. By the end of the lecture and the lab, you'll have written one of these yourself and watched an agent work from it.

Quick show of hands, just to calibrate: how many of you have ever asked an agent to build something, gotten back something subtly — or not so subtly — wrong, and then spent longer explaining what you actually meant than it would have taken to just write it down up front? Keep that memory close. That's the entire motivation for this module, and we're going to name exactly why it happens and what you do instead.

---

## Slide 2 — Agenda

**[~2 min]**

Here's the shape of the next two hours. We'll start with why ambiguity is the single biggest tax you pay when working with an agent — not a minor annoyance, the *number one* cost driver. Then we get concrete: the actual anatomy of a spec that an agent can execute against, section by section, with a worked example we'll build up piece by piece. After that, we look at the full loop — spec, plan, implementation, and the step everybody skips: updating the spec afterward. Then we'll draw a hard line between two documents people constantly conflate: repo-level agent docs like CLAUDE.md or AGENTS.md, versus a feature spec. We'll cover the common pitfalls — the ways teams get this wrong even after they've bought into the idea. And then you're doing it yourself in the lab: write a real spec, hand it to an agent with nothing else, and find every place the spec had a hole.

Nothing here is abstract theory for its own sake. Every section maps directly onto something you'll do in the lab in about an hour.

---

## Slide 3 — Objectives

**[~2 min]**

Let's be precise about what "done" looks like for this module, because DDD is one of those topics where it's easy to nod along and then not actually change how you work.

By the end, you should be able to do five concrete things. First, use a written spec as a *contract* — not a suggestion, not a vibe, a contract the agent implements against. Second, tell the difference between a spec that's too vague and one that's over-specified — both are failure modes, and they're opposite failure modes, so you need to recognize both directions of the error. Third, run the *full* DDD loop, including the step teams reliably skip — updating the spec afterward. Fourth, treat the spec as a living artifact rather than a one-time handoff you write and then forget about. And fifth — this one matters as much as the other four — recognize when DDD is *not* the right tool. This module is not "always write a spec for everything." We'll give you a decision framework near the end for when a spec is overkill.

If you leave today able to do those five things, the module worked.

---

## Slide 4 — The problem DDD solves

**[~8 min]**

Let's name the disease before we talk about the cure. The single biggest source of wasted agent turns — and I mean this is not an exaggeration, if you tracked your own time this would likely be your largest line item — is ambiguity.

Here's the mechanism. You ask an agent to build something. Your request is underspecified — maybe you thought it was clear, but it wasn't, because you were holding a bunch of context in your head that never made it into the words you typed. The agent doesn't have your head. It has your words. So it does the only thing it can do: it guesses at your intent, using whatever priors it has from its training and from whatever context is in the repo. Sometimes it guesses right. Often, on anything with real ambiguity, it guesses at *something plausible* that is not what you wanted.

Now you're in the expensive part. You look at what it built, you realize it's not right, and you start explaining what you actually meant. And here's the sting: that correction conversation frequently takes *longer* than it would have taken to just write the intent down once, up front, before the agent touched any code. You're paying for the ambiguity twice — once in the wrong output, once in the correction — when you could have paid for it once, cheaply, as a few minutes of writing.

There's a second cost that's easier to miss: that conversation where you "explained it" to the agent — it leaves no durable trace. It happened in a chat window. Nobody is going to reread that chat log in three weeks when they're wondering why the export button behaves the way it does. Compare that to a spec file sitting in the repo — that's discoverable, greppable, reviewable in a pull request, and useful to the next person, human or agent, who touches this feature.

So here's the reframe DDD is built on: front-load that cost into a *document* instead of a *conversation*. Writing the spec takes real time — I'm not going to pretend it's free — but you do it once, you keep the artifact, and it pays down the ambiguity tax before the agent ever starts guessing instead of after you discover it guessed wrong.

---

## Slide 5 — What is Document-Driven Development?

**[~8 min]**

So, formally: Document-Driven Development means a written spec is the *primary interface* between the human and the agent for a piece of work. Not the primary interface among several — the primary one. If there's a conflict between what you said out loud in a stand-up and what the spec says, the spec wins, and if the spec is wrong, you fix the spec, you don't just let the verbal version quietly override it in someone's memory.

Given that spec, here's what the agent actually does, in four steps. One: it reads the spec. Two: it plans against it — meaning before writing code, it produces a plan for how it intends to satisfy the spec, and you get to look at that plan before any code exists. Three: it implements against the spec, building to what's written. And four — and I want you to really sit with this fourth one — it helps you *update* the spec when reality diverges from the plan.

That fourth step is the one that almost every team skips, and it's also the one that makes this "document-driven" rather than just "we wrote a doc once and then ignored it." Here's why it matters so much: specs are written *before* you've actually built the thing, which means they're written with incomplete information. You will discover things during implementation — an edge case nobody thought of, a constraint from an existing API, a decision that turns out to be wrong once you see it running — that the spec didn't anticipate. If you don't feed that discovery back into the document, the spec now describes a system that doesn't exist. It's describing the *plan*, not the *product*. Anyone who reads it later — including future-you, including the next agent session — is being actively misled by a document that looks authoritative but isn't accurate anymore.

So hold onto this: DDD is not "write a doc, then code." It's a loop that includes writing back into the doc. We'll come back to this exact point in a few slides because it's genuinely the crux of the whole module.

---

## Slide 6 — Anatomy of a spec — overview

**[~10 min]**

Let's get concrete. What actually goes into a spec that an agent can execute against? There are six sections, and I want to walk through why each one exists before we look at a worked example.

One — **Goal**. One paragraph, plain language, describing what problem this solves. Not a feature list, not a technical design — just: here's the problem, here's what "solved" looks like.

Two — **Non-goals**. This is the one people most often skip, and it's arguably as important as the goal itself. Non-goals are explicit statements of what's *out* of scope. We'll spend a whole slide on why these matter.

Three — **Interfaces / contracts**. This is anything the agent must *not* invent on its own — function signatures, API shapes, data models, button labels, file naming conventions. If it's load-bearing and you don't write it down, the agent will invent something, and its invention becomes the de facto contract that everyone downstream has to live with.

Four — **Edge cases**. The ones you already know about. Not hypothetical exhaustive edge-case brainstorming — specifically the ones sitting in your head right now that you already know are going to come up.

Five — **Acceptance criteria**. Testable statements, ideally literally expressible as commands or tests that either pass or fail. This is what turns "is this done?" from an opinion into a checkable fact.

Six — **Open questions**. This is the section people are most surprised to see in a spec, because it seems to contradict the whole "specs remove ambiguity" premise. It doesn't — it's how you leave certain decisions deliberately open, on purpose, for the agent to propose an answer to, rather than either guessing silently or forcing you to decide something you don't have enough information to decide yet.

We're going to build all six of these live, using one worked example: a CSV export feature for a reports dashboard. It's deliberately mundane — I want you to see spec-writing applied to something ordinary, because most of your specs in real life will be for ordinary features, not exotic ones.

---

## Slide 7 — Goal + Non-goals

**[~8 min]**

Here's the Goal section for our CSV export feature: "Let a user export the currently filtered report rows to a CSV file, matching the date range they've already selected on the dashboard." Read that again — notice what it does and doesn't say. It says what problem is being solved — user wants their filtered data out of the dashboard and into a file. It does *not* say which library to use, what the button's exact pixel position is, or how the CSV gets generated internally. That's intentional. The goal is the "why," stated in plain language, short enough that anyone skimming the doc gets the point in five seconds.

Now the Non-goals: "No new file formats — CSV only, not XLSX or PDF" and "No server-side scheduled or emailed exports — synchronous, on-click download only." Look at what these two lines just did. Without them, here's a very plausible thing that happens: the agent, being helpful, notices that Excel export would be a nice adjacent feature, or notices there's an existing email-sending utility in the codebase and figures a scheduled export would round things out nicely. Maybe it's right that those would be nice! But they weren't asked for, and now you've got scope creep that came from a well-meaning agent trying to be thorough.

This is why I said non-goals are as load-bearing as the goal itself. They're not padding. They're not boilerplate you add because a template told you to. Every non-goal you write is a specific guardrail against a specific plausible misstep — often one you can picture happening because you've watched an agent do it before, or because it's the natural next feature a human developer would also assume goes together.

Practical tip when you're writing your own specs later today: after you write the goal, spend thirty seconds asking "what's the adjacent, plausible-sounding feature someone might assume I also want?" That question is where your non-goals come from.

---

## Slide 8 — Interfaces / contracts

**[~8 min]**

Next section: interfaces and contracts. For our CSV export, the spec says: a button labeled "Export CSV" next to the existing date-range picker; clicking it downloads a file named `report_<start>_<end>.csv`; and the columns match the currently visible table columns, in the same order.

Notice how specific this is compared to the goal. The goal was intentionally loose — plain language, one paragraph. The interface section is intentionally tight — exact button label, exact filename pattern, exact column ordering rule. That's not inconsistency, that's the whole design of a good spec: be loose where looseness doesn't cost you anything, and be precise exactly where precision prevents a real problem.

Here's the line I want you to remember from this slide: if it matters, and you don't write it down, the agent invents it — and its invention becomes the de facto contract that the next reader has to reverse-engineer. Think about what that actually means in practice. Say you didn't specify the filename format. The agent picks something reasonable — maybe `export.csv`, maybe `report-2024-01-15.csv` with today's date instead of the range. It ships. Three weeks later someone builds an automated test that downloads the file and checks its name, and now *that* filename — the one the agent happened to pick — is the contract, whether anyone chose it deliberately or not. Nobody decided that filename format. It just... became true, by accretion, because nobody wrote down what they actually wanted.

So the test for "does this belong in the interfaces section" is: if two different competent engineers — or two different agent runs — might reasonably make different choices here, and the choice matters to someone downstream, write it down. If it truly doesn't matter which way it goes, leave it out; you don't need to specify things nobody will ever depend on.

---

## Slide 9 — Edge cases

**[~7 min]**

Edge cases. For the CSV export: no rows in the selected range should produce a header-only CSV, not an error. A date range that spans a daylight-saving-time transition should use UTC dates in both the filename and the date columns, to avoid off-by-one-day bugs. And if the user has an active column filter — not just a date-range filter — the export needs to respect that too, not only the date range.

Here's the thing about every single one of these: you already knew them. Nobody in this room needs a training course to realize that "what if there's no data" is a case worth handling, or that timezone boundaries cause off-by-one bugs, or that if your dashboard has two kinds of filters, an export feature probably needs to respect both. These aren't exotic discoveries — they're the stuff that occurs to any experienced developer within the first thirty seconds of thinking about the feature.

Which is exactly why not writing them down is such a waste. Writing them into the spec costs you almost nothing — you already had the thought, it takes ten seconds to type a sentence. *Not* writing it down doesn't save you that ten seconds — it just relocates the cost. Instead of paying it now, as a line in a document, you pay it later, as a bug report, a confused user, a debugging session, and then — eventually — the same fix, except now it's happening under time pressure with a support ticket attached instead of calmly while you're writing a doc.

I want to be precise about the boundary here, because someone will ask: this section is not "brainstorm every conceivable edge case exhaustively until you're both exhausted." It's specifically the ones you *already know about*. If you find yourself spending twenty minutes trying to imagine edge cases you have no evidence will ever occur, you've left this section and wandered into something else — over-specification, which we'll get to as a pitfall later. Write down what you know. Leave the rest to acceptance-criteria testing and to the open-questions section, which is coming up next.

---

## Slide 10 — Acceptance criteria + Open questions

**[~10 min]**

Acceptance criteria, for our export feature: exporting a known three-row range produces exactly those three rows plus a header — a concrete, checkable number. Exporting an empty range produces a header-only CSV, not a 500 error — directly testing the edge case from the last slide. And the filename matches the `report_<start>_<end>.csv` pattern using UTC dates — again, directly testing something from the interfaces section.

Notice what's happening structurally here: acceptance criteria aren't a new, independent list you brainstorm from scratch. They're the *checkable version* of everything you already wrote in the goal, the interfaces, and the edge cases. Every promise you made earlier in the doc should have a corresponding line here that lets someone — a human or an agent — determine pass or fail without having to interpret anything. That's the test for whether a criterion is well-written: can it be checked mechanically, ideally by an actual command or test, or does checking it require a judgment call? If it requires judgment, it's not really an acceptance criterion yet — it's still a goal in disguise, and you should push on it until it's checkable.

Now, open questions. Ours has one: should the export button be disabled, versus hidden, when there's no data? And notice the second half of that line — "leaving this to the agent to propose in the plan step." This is the section that surprises people, because it looks like it's reintroducing the exact ambiguity we spent this whole lecture arguing against. It isn't, and here's the distinction that matters: there's a difference between ambiguity you *didn't notice* and ambiguity you *deliberately chose to leave open*.

An unmarked gap in your spec is a landmine — the agent hits it, has no signal that you thought about it at all, and guesses silently, and you find out what it guessed only when you review the output. A marked open question is completely different — you're telling the agent "I see this decision, I don't have a strong opinion yet, propose an answer as part of your plan, and I'll look at it before you build." That's not sloppiness, that's an explicit, deliberate handoff, and it's exactly the difference between "the spec was silent" and "the spec spoke and said 'you decide, but tell me first.'" Marking open questions explicitly is what keeps a spec from turning into a straitjacket that pretends to have already decided everything, when really some things are better decided once the agent has looked at the code.

---

## Slide 11 — The loop

**[~7 min]**

Now let's zoom out from anatomy to process. Here's the full loop: write spec, agent proposes a plan against it, human approves or edits the plan, agent implements, verify against acceptance criteria, and then — update the spec to match what was actually built, or, if the build strayed for a bad reason, fix the build to match the spec instead.

Read through those six steps again and notice something about the first four plus verification: write, plan, approve, implement, verify — nobody in this room is going to argue with any of that. That's basically how competent teams work already, agent or no agent. It's obvious. It's also, not coincidentally, the part teams actually do.

It's the sixth step — update the spec — that gets skipped almost universally. Not because anyone disagrees it's a good idea in principle. It gets skipped because by the time you're at step six, the feature works, everyone's satisfied, there's a next task waiting, and going back to edit a markdown file feels like busywork compared to shipping the next thing. I want to flag that feeling right now, because we're about to spend the entire next slide explaining why that feeling is wrong, and it's worth having named it while it's fresh.

---

## Slide 12 — Why the last step is the whole point

**[~8 min]**

Here's the case for why skipping that last step doesn't just leave value on the table — it actively makes things worse than not having written a spec at all.

A spec that silently drifts from the code is worse than no spec. Read that claim carefully, because it's stronger than "a stale spec is not very useful." No spec at all is a known-empty signal — anyone reading the code without a spec knows they have to go figure things out from the code itself, and they do. A *stale* spec looks authoritative. It has headers, it has acceptance criteria, it reads like someone thought carefully about this feature — and it's wrong. It actively misleads the next reader, human or agent, who trusts it and builds on top of an inaccurate premise. You've converted a document that should be a source of truth into a source of *convincing* falsehood, which is strictly worse than an absence of documentation.

So: "update the spec" needs to be in your team's definition of done, the same way tests are. Nobody ships a PR with failing tests and calls it done. The same standard should apply here — if the spec still describes the pre-implementation plan and the implementation diverged from that plan, the work isn't done yet, even if the code is merged and the feature works.

And here's the deeper point, the one I most want you to leave with: the value of DDD doesn't come from having a document sitting in your repo. Lots of teams have specs sitting in repos that nobody's opened in eight months — that's not DDD, that's just filing cabinet behavior. The value comes specifically from the *plan being checked against the spec before implementation happens*. That's the moment where ambiguity gets caught cheaply, before code exists, before anyone's emotionally invested in a particular implementation. If you get that one moment right — plan reviewed against spec, before code — and then let the spec go stale afterward, you've captured most of the value. But if you also update the spec afterward, you've captured all of it, and you've set up the *next* feature's spec review to be even cheaper, because the state of the world it's checked against is accurate.

Short version, and this is worth writing on your own wall: DDD does not mean "I wrote a doc once." DDD means the doc stays true.

---

## Slide 13 — Repo-level agent docs vs. feature specs

**[~7 min]**

Let's clear up a confusion that trips people up constantly: repo-level agent docs — things like `CLAUDE.md` or `AGENTS.md` — and feature specs are two completely different documents, and conflating them causes real problems.

Look at the three dimensions on this table. Scope: a repo-level doc covers the whole repository and is standing context — it applies to every session, every feature, forever, until someone changes it. A feature spec covers exactly one piece of work. Contents: the repo-level doc holds conventions, test commands, architectural constraints — the stuff that's true regardless of which feature you're working on today. The feature spec holds goal, non-goals, interfaces, edge cases, acceptance criteria — everything specific to *this* task. Lifecycle: the repo-level doc gets read every session and rarely changes — maybe you touch it a few times a year. The feature spec is written for this task and gets archived or deleted once it ships, or at most kept around as a historical record of a decision.

Why does this distinction matter practically? Because if you don't separate them, you get two bad outcomes. Either your repo-level doc balloons with feature-specific detail that goes stale the moment that feature evolves — now your "standing context that's read every session" is full of noise about a CSV export button from six months ago. Or your feature specs keep re-explaining repo-wide conventions that should have been said once, at the repo level, and now every spec is longer than it needs to be and any change to a convention means editing a dozen specs instead of one file.

To be clear about scope for this course: when we say DDD in this module, we mean the second kind — the feature spec. That's the artifact the lab is going to have you write.

---

## Slide 14 — Good repo docs make specs shorter

**[~6 min]**

Here's a concrete illustration of why keeping those two documents separate actually pays off, not just organizationally but in how much you have to type.

Imagine your `CLAUDE.md` has this rule already in it: "Before any UI or styling work, read `design/tokens.css` and `design/system.md`. Do not introduce new colors, fonts, or spacing values outside the tokens file." That's a repo-level constraint. It's true for every UI feature this team will ever build, not just this one.

Now look at what that buys you: the CSV-export spec we've been building all lecture never has to mention design tokens at all. Not one line. The spec doesn't need a section saying "use the existing color palette" or "match the existing button styling conventions" — that's already handled, once, at the repo level, and it applies automatically to this feature and every future feature without anyone having to remember to restate it.

That's one less thing to write in every single spec you produce from now on, and — this is the part people undervalue — one less thing that can go stale *inside* a feature spec. If your design tokens change next quarter, you update `design/system.md` once. You don't have to hunt down every historical feature spec that happened to mention colors and update them all. This is the practical payoff of getting the separation from the last slide right: good repo-level docs are a force multiplier that makes every future feature spec shorter, and shorter specs are cheaper to write, cheaper to review, and cheaper to keep accurate.

---

## Slide 15 — Common pitfalls (1 of 2)

**[~6 min]**

Let's talk about how this goes wrong in practice, even for teams that have bought into the whole idea. Two pitfalls here, two more on the next slide.

First: **stale docs**. This is the one we already built a whole slide around — spec says one thing, code does another, and nobody notices until it causes an actual bug, at which point someone's debugging a mismatch they didn't know existed. The mitigation is exactly what we said before: "update the spec" is part of your definition of done. Not a nice-to-have, not something you do if you have spare time at the end of the sprint — part of done, checked the same way you'd check that tests pass.

Second: **over-specifying**. This is the opposite failure mode, and it's just as real. This is when a spec starts dictating implementation details that genuinely don't matter to anyone — internal variable names, which specific helper function does the string formatting, exact code structure that has no external effect. This is expensive twice over: it's expensive to write, because now you're spending your spec-writing time on decisions nobody needed you to make, and it's expensive to keep in sync, because implementation details change far more often than behavior does, so an over-specified doc goes stale faster and more often. The mitigation: specify contracts and behavior — the things someone else, human or agent, needs to rely on — not internals, *unless* the internals genuinely are the point of the task. If you're writing a spec for a performance optimization, then yes, internals might actually be the point, and you specify them. For a CSV export button, they're not, and you don't.

---

## Slide 16 — Common pitfalls (2 of 2)

**[~6 min]**

Two more.

Third pitfall: **under-specifying known edge cases**. We covered the mechanism already back on slide 9, but it's worth restating as a pitfall in its own right because it's so common: if you know about an edge case and you don't write it down, you have not saved time. You have moved the cost from "spec-writing," where it's cheap, to "debugging," where it's expensive and happens under worse conditions — often in production, often reported by a confused user rather than caught by you calmly at your desk.

Fourth pitfall: **treating the spec as a one-way handoff**. This is a team writing a genuinely good spec, handing it to the agent, and then walking away until the code is done — skipping the plan-review step entirely. This defeats a huge part of the purpose. Remember what we said on slide 12: the value of DDD comes specifically from the agent's plan being checked against the spec *before* implementation starts, not from the spec merely existing somewhere. If you file the spec and vanish, you've given up the cheapest, earliest point at which you could have caught a misunderstanding — before any code was written — and you're back to catching problems only after the fact, which is exactly the expensive pattern DDD exists to avoid.

Notice something about all four pitfalls across these two slides: none of them are "DDD doesn't work." Every one of them is a team doing DDD halfway — skipping the update step, going too far in one direction on detail, knowing something and not writing it, or checking out of the review step. DDD done fully avoids every one of these. DDD done partially reproduces most of the pain it was supposed to eliminate.

---

## Slide 17 — When DDD is the wrong tool

**[~8 min]**

Now the piece that keeps this module honest: DDD is not the right tool for every situation, and pretending otherwise would make you worse at your job, not better.

Look at this table across four methodologies. DDD, spec-first, is best for features with real ambiguity and multi-person context — situations where more than one person, or more than one session, needs a shared, durable understanding of what's being built. It's weak for tiny fixes, where writing a spec is pure overhead relative to the size of the change. What it leaves behind is a durable spec document.

Plan-first is a lighter-weight cousin — good for refactors and risky multi-file changes where you want a plan reviewed before the agent touches a dozen files, but you don't need the full spec apparatus. It's weaker for fast exploration, where even a plan is too much ceremony. It leaves behind an ephemeral plan or an ADR, not a durable spec.

TDD-with-an-agent is a different axis entirely — you lead with tests rather than a prose spec, which is excellent for bug fixes and well-defined logic where the correct behavior is easy to state as a test case. It's weak for vague or exploratory UI work, where "what should this look like" isn't something a test can capture well. It leaves behind a test suite as the artifact.

And conversational — no spec, no plan, just talking it through — is genuinely the right choice for prototypes and one-offs, where the cost of any documentation exceeds the value of the thing you're building. It's weak for anything needing a paper trail, and, unsurprisingly, it leaves nothing behind.

The rule of thumb to internalize: a five-line bug fix does not need a spec. Writing one would be pure overhead — you'd spend more time writing the document than fixing the bug, and there's no real ambiguity to front-load a cost against in the first place. A feature with real ambiguity does need one — that's the exact situation where the cost of writing a paragraph now is smaller than the cost of a wrong guess later. Learning to tell those two situations apart quickly is arguably a more valuable skill from this module than the mechanics of spec-writing itself.

---

## Slide 18 — Lab: write a spec, hand it to an agent

**[~5 min, then hands-on]**

Here's what you're doing for the rest of this session. Six steps.

One: pick a real, small-to-medium feature — either from the sample repo provided for this course, or bring your own if you've got something in flight that's a good fit. Small-to-medium matters here — not a five-line fix, per the last slide, but not something so large it can't fit in the lab time either.

Two: write a one-page spec using the anatomy we walked through — goal, non-goals, interfaces, edge cases, acceptance criteria, open questions. And time yourself. I mean this literally — note your start and end time. You'll want that number for the deliverable.

Three: give the agent *only* the spec as the task. No verbal context, no "oh and also," no filling in gaps out loud after you hand it over. This constraint is deliberate and it's the whole point of the exercise — if you cheat and give verbal context on the side, you'll never find out where your spec was actually silent, because you'll have patched the silence with your voice instead of with the document.

Four: have the agent propose a plan *first* — don't let it go straight to implementation. Review that plan against your spec before you approve anything. This is the step from slide 11 and 16 that gets skipped in the real world — don't skip it here, because this is where you're going to catch the most interesting gaps.

Five: after implementation, check actual behavior against your acceptance criteria, one by one.

Six: update the spec to close every gap you find. Don't just note the gaps mentally — actually edit the document. That edit is the DDD loop closing, and it's graded, informally, by whether you actually did it or just intended to.

Go ahead and get started — I'll circulate and answer questions.

---

## Slide 19 — Lab: what to watch for

**[~4 min — deliver before or during lab circulation]**

While you're working, here are four specific things to pay attention to, because they're the signal, not the noise.

First: every place the agent had to *guess* — that's a direct measurement of where your spec was silent. Don't get defensive about it; that's the data you came here to collect.

Second: every place the plan *surprised* you — go back to the plan-review step. If something in the agent's proposed plan made you go "wait, that's not what I meant" — good, you caught it before any code existed, which is the entire point of reviewing the plan first instead of just reviewing the diff afterward.

Third: every acceptance criterion that fails on the first try — and here's the more interesting question to ask yourself when that happens: is the *code* wrong, or was the *criterion* itself unclear or wrong? Don't assume it's automatically the code's fault. Sometimes you'll find your own acceptance criterion was ambiguous or actually specified the wrong behavior, and that's just as valuable a finding as a code bug.

Fourth: be honest with yourself about time spent — writing the spec, reviewing the plan, checking acceptance criteria, all of it. This is the number that lets you later judge, for real, whether DDD paid for itself on a task of this size, rather than relying on a vague feeling about whether it was worth it.

---

## Slide 20 — Deliverable

**[~3 min]**

Here's exactly what you're turning in, or what you should have at the end of the lab even in a self-paced setting. The spec document itself. The agent's plan, if you used plan mode. The resulting diff. And a short list — this is the one I want you to take most seriously — titled something like "places the spec was wrong or incomplete, and what I changed."

That last list is the artifact that matters most out of all four. Here's why: the spec document alone just shows you produced *a* spec — it doesn't tell you or anyone else whether that spec was any good. The gap list is direct, honest evidence of what your spec was actually worth on a real task. It's the difference between "I wrote a spec" and "I wrote a spec, and here's precisely where it held up and where it didn't." If your gap list comes back mostly empty, that's either a sign you wrote an excellent spec or a sign you weren't looking hard enough — and if it's long, that's not a failure, that's exactly the learning signal this exercise exists to produce.

---

## Slide 21 — Recap + next up

**[~3 min]**

Let's land the plane. Three things to take away from today.

A spec is a *contract*, not a wish list — it's the thing the agent is accountable to, and the thing you hold the implementation against.

The loop only counts as DDD if the spec actually gets updated. Four steps of write-plan-implement-verify are necessary but not sufficient — the update step is what separates DDD from "we wrote a doc once."

And: repo-level docs and feature specs are different tools, used together, not interchangeably. Repo-level docs are standing context that rarely changes; feature specs are scoped, temporary, and specific to one piece of work — and good repo-level docs make every feature spec you write from now on shorter.

Next time, Module 7: Deterministic Design Systems. Same underlying idea — write it down so the agent doesn't guess — applied to a different domain: instead of feature behavior, we're applying it to visual consistency, using design tokens and design docs instead of vague adjectives like "make it look clean." If you found today's "the agent invented something because I didn't write it down" story compelling, you're going to see the exact same story next module, just about colors and spacing instead of CSV filenames.

That's the module. Good luck in the lab — I'll be around for questions.
