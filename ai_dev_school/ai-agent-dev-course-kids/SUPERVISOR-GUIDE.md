# Supervisor Guide (Read This First)

At this age, "supervised" means **present the entire time**, not
checking in periodically. This guide is shorter than the teen course's
because the model is simpler: the adult runs Claude Code, approves
everything it does, and helps with reading/writing/typing wherever the
kid needs it. The kid's job is the idea. Your job is everything around
it.

## Before Session 0: setup

- **One dedicated, empty project folder**, just for this course
  (e.g. `~/kid-ideas`). Nothing else lives there. Same reasoning as the
  teen course: an agent can read/edit anything in its working folder, so
  keep that folder to only what this course creates.
- **No accounts, no logins, no internet-facing anything.** Everything
  built in this course should run and be viewable locally — a local
  webpage, a simple local app. There's no reason at this age to touch a
  real account, an API key, or anything that costs money or is visible
  to strangers.
- **The most restrictive permission setting available.** You (the adult)
  approve every action Claude Code proposes, every session, no
  exceptions. This isn't about the tool being unsafe — it's that reading
  the proposed action out loud ("it wants to make a new file called
  `game.html`, is that right?") is itself part of the lesson.
- **Decide the "show it" method ahead of time.** A simple local web page
  is the easiest thing to show a 7–8 year old their result — it opens in
  a browser and they can see/click things immediately. Know how you'll
  open and refresh it before the first session so it's not a fumbling
  moment mid-session.

## During a session

- **Read everything out loud.** Idea Cards, what Claude Code says it's
  about to do, the result — narrate it. At this age the loop only
  teaches anything if the kid can follow what's happening, not just see
  an end result appear.
- **You type anything beyond the Idea Card's simple blanks.** The kid
  fills in the card's words; you handle opening Claude Code, giving it
  the actual instruction built from the card, approving its actions, and
  opening the result.
- **Keep it to one Idea Card per session.** Resist the urge to let a
  session run long because it's going well — at this age, ending on a
  high note beats squeezing in one more thing.
- **Let the kid react first.** When the result appears, wait for their
  reaction before you say anything. "Is that what you imagined?" is a
  better first question than explaining what happened.

## What to watch for

- **Frustration when the result isn't what they imagined.** This is
  expected and is directly the point of Session 8 (Bug Hunt) — reframe
  it as "let's tell the machine what's different" rather than a failure.
- **Losing the thread of "I wrote this, and that's why it did this."**
  If a session starts to feel like the machine is just producing things
  unrelated to what was asked, pause and reread the Idea Card together
  before continuing.
- **Session length.** 15–25 minutes is the target. If attention is gone,
  stop — there's always a next session, and nothing here is timed.

## What not to worry about

- The Idea Cards being simple, repetitive, or "not real code." That's
  the design, not a limitation — the goal at this age is the loop
  (idea → real thing → reaction → change), not coding vocabulary.
- A kid wanting to skip ahead to a bigger idea before finishing the
  sequence. Sessions 0–9 are short on purpose so that skipping isn't a
  big loss — if they're itching to just build their own big idea, Session
  10 is right there and nothing stops you from doing it early and coming
  back to fill in a skipped session later.

## Sessions 1–3 (doors, notebook, trick): extra notes

- **Session 1 (doors):** only *local* doors to one dedicated folder
  (`facts`), and only *look-only* — deny the server's write tools. No
  internet-facing servers, no accounts, no tokens, ever. A server is a
  program that runs on the computer, so install it yourself, from a source
  you trust, and read aloud what Claude Code asks to run. If you'd rather
  not install anything, the on-paper version teaches the same idea.
- **Session 2 (notebook):** the notebook is a plain file the whole family
  could read. Favorites only — never a full name, address, school, phone
  number, passwords, or other people's names. Check every line before it
  is written, and let the kid see how to erase one.
- **Session 3 (trick):** keep tricks to safe steps — drawing or writing on
  the page. A skill can run commands, so never let a trick include
  running programs or touching files outside the course folder.
