# Lecture Script — Module 15: Capstone: Build & Show

Facilitator notes: this is a spoken script, not a script to read word for
word. Say it like you'd talk to a smart 15-to-17-year-old who has now
done eleven modules of this with you and has actually built things — you
are not introducing anything new today, you are handing the wheel over
completely. Total lecture portion should run **~30-35 minutes**; this is
the capstone, so unlike earlier modules the bulk of the session — likely
the bulk of *several* sessions, since a real capstone rarely fits one
sitting — belongs to the hands-on build, not to you talking. Don't be
afraid to compress the recap section live if the group already knows it
cold. Slide numbers below match `slides.md` exactly.

---

## Opening (~1-2 min)

## Slide 1 — Capstone: Build & Show

Welcome them in. Something like:

"This is it — the last module. Everything up to today was building one
skill at a time: reading what the agent does, writing clear instructions,
specs, plans, tests, review, all of it, one piece at a time so you could
actually absorb each one. Today there's no new piece. Today you take
every single one of those pieces and use them together, for real, on one
project you actually care about finishing. My job today is mostly to get
out of your way faster than usual."

---

## Slide 2 — Today

"Quick shape of the session. We'll spend a few minutes doing something
we haven't really done yet — looking back at the whole arc of this
course, module by module, compressed. Then I'll walk through exactly
what the capstone assignment is: one project, spec, plan, test, review,
tied straight back to Modules 6, 8, 9, and 11. Then some guidance on
picking or finishing a project from whatever track you chose back at the
start. Then what you actually have to hand in. And then — and this is
the important part — most of today is just you building, with me
around if you get stuck."

*(~3 min total so far)*

---

## The Recap (~7-9 min)

This section can run shorter live if the group clearly remembers this
material well — use your judgment. The point isn't testing recall, it's
giving the whole course a shape before they use all of it at once.

## Slide 3 — Recap: Where You Started (0–2)

"Let's rewind all the way to day one. Module 0: an agent isn't
autocomplete, and it isn't magic — it's a partner that takes real,
visible actions in a loop. Module 1: we slowed that loop down and you
tracked it play-by-play — read, write, run, check, repeat. Module 5: the
difference between a vague ask and a clear one, and how a vague ask
just gets you a guess. Those three modules were all about *seeing
clearly* what this tool actually does."

## Slide 4 — Recap: Building the Habits (3–6)

"Then we started building actual habits. Module 6: write a real spec
before anything bigger than a quick fix — goal, not-this, behavior,
done-means. Module 7: write your style down, or every session guesses
differently and your project looks stitched together. Module 8: for
anything touching multiple files, review the agent's plan before it
touches anything, same as agreeing on a route before a road trip.
Module 9: a test that fails first, then a fix that makes it pass — proof,
not just 'looks right to me.' These four are the backbone of everything
you're doing today."

## Slide 5 — Recap: Getting Rigorous (7–9)

"Modules 10 through 12 were about calibration — not every task needs the
heavy process. Module 10: small, exploratory stuff can just be talked
through, no written plan required. Module 11: a completely fresh second
agent, with no memory of how something was built, catches things the
builder is blind to — like swapping papers with a classmate before
turning something in. Module 12: agents sound confident even when they're
wrong, so you're the one doing the actual checking, every time."

## Slide 6 — Recap: Owning It (10–11)

"And the last two, before today, were about ownership. Module 13:
automate what you've proven works, but keep an approval gate on
anything that isn't fully reversible. Module 14: your own AI use
policy — how you use it, how you disclose it, and what you never let
yourself skip understanding, even under time pressure. That policy
you wrote isn't decoration. You're about to actually use it, today, for
the walkthrough."

*(~11-12 min total so far)*

---

## The Capstone Assignment (~8-9 min)

## Slide 7 — The Capstone, In One Line

"So here's today, in one sentence: one real project, every habit from
this course, used together, for real, on something you actually want to
finish. Not a new skill — I'm not teaching you anything new today. Not
a toy exercise built just to demonstrate a technique, the way some of
the earlier hands-on tasks were. The actual thing, built the way you
now genuinely know how to build it."

## Slide 8 — Pick Your Project

"Whatever track you picked at the start of the course still applies —
personal site, small game, bot, or a tool for your school club. Here's
what 'finished' looks like for each: a site means multiple pages with
one consistent design, not three pages that each look like a different
project. A game means a few mechanics actually working *together*, not
just one isolated demo. A bot means a handful of commands that actually
work and are actually tested. A club tool means something the club can
genuinely pick up and use, not just something that ran once on your
machine.

And to be clear — the thing you've been building since Module 6 counts
completely. If you want to start something fresh instead, that's fine
too. Nobody's docking points either way."

## Slide 9 — Finish Beats Perfect

"One piece of advice before you start scoping today, because I've
watched this go wrong before: pick something you can actually finish in
the time you've got, not the biggest version of the idea living in your
head. A small, finished, tested thing beats a huge, half-built,
untested one — every single time, for what this checkpoint is actually
measuring.

If you're running the numbers and you're not sure it all fits — cut a
feature, don't cut testing or review. Those two are the entire point of
today. And if you've got ideas you're excited about but don't have time
for, that's exactly what the 'not this' section of your spec is for.
Write it down, don't build it today."

## Slide 10 — The Four Moves

"Here's the actual structure, and you already know every piece of it.
Spec it — that's Module 6. Plan it — Module 8. Test the core logic —
Module 9. Get it reviewed — Module 11. Same four moves you've each done
separately already. Today you run all four, back to back, on one real
thing, start to finish."

*(~19-21 min total so far)*

---

## Walking Through the Four Moves (~8-9 min)

## Slide 11 — Move 1 — Spec It

"Move one, same four sections as Module 6. Goal — what this is
supposed to do, plain language, no jargon for jargon's sake. Not this —
what's explicitly out of scope, so the agent doesn't 'helpfully' wander
off and build things you didn't ask for. How it should behave — the
important cases, especially the tricky ones you already know are
tricky. Done means — how you, or literally anyone else, would know it
actually works.

Here's the real test of a good spec: could someone who never talked to
you about this project read it and actually get what it's supposed to
do? If the answer's no, it's not done yet."

## Slide 12 — Move 2 — Plan It

"Move two. Hand the agent your spec, and before any big edits happen,
use plan mode — have it propose its approach. Which files, in what
order, what it thinks it needs to touch. Then actually read that plan.
Not skim it — read it. If something's missing, or it's planning to
touch a part of the project it has no business touching, push back
right there, before anything changes. Only approve once the plan
actually makes sense to *you*, not just once it sounds reasonable."

## Slide 13 — Move 3 — Test the Core Logic

"Move three. Not coverage for coverage's sake — the part that actually
matters if it breaks. The scoring function. The command parser. Whatever
the rest of your project depends on being right. If you can honestly
say a specific test would have caught a real bug you've actually seen —
that's the gold standard, and it's worth aiming for. Remember Module 9's
whole point: 'looks right' and 'a test proves it's right' are not the
same claim, and the gap between them is exactly where bugs like to
hide."

## Slide 14 — Move 4 — Get It Reviewed

"Move four, and this is the one people are most tempted to fake. A
genuinely brand-new session — not you asking the same session 'hey, does
this look okay,' an actual fresh start with zero memory of how you built
it. Give it only the finished result and your spec. Not the story of how
you got there, not your reasoning, not your excuses for the messy part.
Ask it to check the build against the spec — not against what you meant,
against what you actually wrote down. And write down what it finds,
even the small stuff, even if it stings a little."

*(~28-30 min total so far)*

---

## Closing the Loop and the Deliverable (~7-8 min)

## Slide 15 — If It Has Any UI: Stay Consistent

"Quick one, and it only applies if your project has any interface at
all. Module 7's rule is still live — colors, fonts, spacing come from
your written style sheet, not a fresh guess each screen. A capstone
where three screens look like three unrelated projects is a completely
avoidable miss, and it's one people make when they're rushing at the
end. If you're building a bot or a command-line tool with zero visual
interface, this slide doesn't apply to you — skip it and move on."

## Slide 16 — Close the Loop

"Whatever the review actually caught, fix it — don't rubber-stamp your
own work just because you're tired and it's late in the session. And if
the review revealed your spec itself was wrong or missing something,
update the spec too, not just the code. The spec is supposed to be the
source of truth for this project. If it's out of date, it's lying, even
if nobody meant it to. This step is the one that gets skipped under time
pressure more than any other — don't let it be the one you skip."

## Slide 17 — Deliverable: Three Things

"Here's exactly what you're handing in, and it's three separate things,
not one. One: the finished project, actually working, not 'basically
working, trust me.' Two: your artifacts — the spec, the plan, the tests,
the review notes — saved as real files, not just something you remember
doing. Three: a short walkthrough, written or spoken, whichever you'd
rather do.

All three, together. A genuinely great project with no saved spec
doesn't clear the bar today — the artifacts are half the point of this
whole exercise."

## Slide 18 — The Walkthrough

"The walkthrough covers three things, and I want you to actually be
honest here, not polished. What you built. What the agent did versus
what you did yourself — specifically, concretely, not 'it helped a
lot.' And one thing that surprised you, across this entire course, not
just today.

This is your Module 14 policy, in action, for real, for the first time
where it actually matters. If your policy said you'd be honest about the
agent's role — this is the moment that gets tested."

*(~37-40 min if run at full length — cut the recap section shorter live,
or move faster through Moves 1-4 if this group already has strong
habits, to land closer to the 30-35 minute target and protect build
time.)*

---

## Self-Check and Handing Off (~3-4 min)

## Slide 19 — Self-Check Before You Call It Done

"Before you call anything finished today, run it against these five
questions, out loud or in writing. Could someone else read your spec
and understand the project with zero explanation from you? Did the
actual build match the plan you approved — and if it didn't, do you
know *why* it didn't? Do your tests check the behavior that actually
matters, or just the easy happy path that was never going to break
anyway? Did the review catch something real, or did you wave it through
without really looking? And is your walkthrough honest about the
agent's role, per your own policy?

If you get an uncomfortable answer to any of these — good. That's the
checkpoint doing its job. Fix it before you call it done, not after."

## Slide 20 — Your Turn: Hands-On

"Okay — that's everything. Here's the actual sequence: confirm your
project and your scope for today. Write the spec. Plan mode, review it,
approve it. Build, then test the core logic. Open a completely fresh
session and get it reviewed. Fix whatever it caught, and update the
spec if it needs it. Write your walkthrough.

I want to be upfront: this can run long, and that's completely expected.
This is the capstone — if it takes more than one session to actually
finish this properly, that's not a failure, that's just what a real
project takes. Go."

*(~40-44 min total if the full script is used — expect to trim live;
the hands-on build is the actual point of today, likely spanning more
than one session)*

---

## Wrap-Up, Whenever the Build Session Ends

## Slide 21 — Recap

"Whenever you wrap for the day — or for good, if this is it — here's
what today was. Same four moves you already knew: spec, plan, test,
review, now used together, for real, on one thing. Finished and honest
beats big and half-built. The deliverable was three things: the project,
the saved artifacts, and an honest walkthrough. And the self-check
questions exist so you're the one who catches a rubber-stamped review,
before anyone else has to."

## Slide 22 — You Made It

"Twelve modules ago, some of you genuinely weren't sure this was
anything more than fancy autocomplete. Today you wrote a spec, reviewed
a plan, wrote a real test, sent your work to a second agent that owed
you nothing, and can now stand here and tell me exactly what you built
versus what it built. That gap — being able to say precisely where you
end and the tool begins — is the actual skill this whole course was
built around. Everything else was practice for this moment.

Go show someone what you built. You earned that part."

---

*(Total lecture time if delivered in full: roughly 40-44 minutes as
scripted. Trim the recap section and move briskly through Moves 1-4 for
groups that already have these habits solid, to land closer to the
30-35 minute target — the goal is protecting real build time, which for
a genuine capstone will likely span more than one session.)*
