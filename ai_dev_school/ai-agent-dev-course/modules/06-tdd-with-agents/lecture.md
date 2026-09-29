# Module 6 — Lecture Script: Test-Driven Development with Agents

*Speaker notes. Read the slide headers aloud as you advance; the text under
each heading is what you actually say. Bracketed notes are stage directions,
not narration.*

---

## Section: Opening & Framing (Slides 1–3) — ~10 min

### Slide 1 — Module 6 / Test-Driven Development with Agents

Good morning, everyone. Welcome to Module 6. Today's topic is Test-Driven
Development with agents, and the case study running through the whole
session is "tests as the spec."

That subtitle is doing a lot of work, so let me say it plainly up front:
by the end of today, I want you to walk away believing that a well-written
failing test is the single best instruction you can hand an AI coding
agent — better than a paragraph of prose, better than a ticket description,
better than a verbal explanation. We're going to spend the next couple of
hours proving that to you with a live worked example, not just asserting
it.

[Pause. Let that land.] If you've done TDD before, some of this will feel
familiar — red, green, refactor, you know the drill. What's new is the
second half of every step: not just "does the agent do this," but "how do
you verify the agent did this *for the right reason*." That's the part
that's specific to working with agents, and it's the part most people skip
the first time.

### Slide 2 — Agenda

Here's the shape of today. We'll start with why tests beat prose as a
specification, specifically when the reader is a language model instead of
a person. Then we'll walk through red-green-refactor with an agent doing
the driving, and we'll do it with an actual bug — a real off-by-one in a
discount calculation — start to finish, so you see every step, including
the ones that are easy to skip.

After that we'll contrast two flavors of test as spec: example-based tests,
which you've all written, and property-based tests, which fewer of you
have. We'll talk about why the combination matters more with an agent in
the loop than it does when you're coding solo.

Then we'll talk directly about hallucination — what it actually looks like
in this context, and why the mechanism of a failing test specifically
interrupts it. And we'll close with a lab where you get nothing but a bug
report and have to run the whole loop yourselves.

### Slide 3 — Learning Objectives

Three objectives for today. First, you should leave able to use tests as
an executable, unambiguous spec for an agent — not as an afterthought you
write once the code is "done," but as the very first artifact you produce.

Second — and this is the conceptual core of the module — you should
understand *why* a failing test written before the fix reduces agent
hallucination. Not just that it does, but the mechanism. We'll come back to
this multiple times today because it's easy to nod along and harder to
actually internalize.

Third, I want you to know when this technique is the right tool and,
just as importantly, when it isn't. TDD-with-agents is not a universal
hammer. There are whole categories of work where writing the test first is
actively the wrong move, and a good engineer — or a good user of an agent —
knows the boundary.

---

## Section: Why TDD Matters More & the Loop (Slides 4–6) — ~20 min

### Slide 4 — Why TDD Matters Even More With Agents

Let's start with a claim that might surprise some of you: TDD matters
*more* with an agent than it does with a human developer, not less.

Think about why humans do TDD. For a human, TDD is mostly a discipline
problem. You *know* how to verify your code works — you can reason about
it, step through it mentally, run it in a debugger. TDD's value for a human
is that it keeps you honest, keeps you focused on small increments, and
gives you a regression net. But if you skip it, you're not helpless — you
still have judgment you can fall back on.

For an agent, it's a different kind of problem. It's a targeting problem.
The model is very good at producing plausible, confident-sounding code.
What it doesn't have is your judgment about whether "plausible" and
"correct" are actually the same thing in this specific case. So when you
hand an agent a prose specification — "fix the bug where bulk discounts
don't apply correctly" — you have handed it something that can be
satisfied on the letter while completely missing the intent. The agent
can produce a change, explain the change persuasively, and be wrong, and
nothing in that process forces a correction.

A failing test closes that gap. A failing test has exactly one legitimate
way to turn green: the underlying behavior has to actually change to match
the assertion. You can't talk your way past an assertion. You can't be
persuasively wrong to a test runner. That asymmetry — prose can be
satisfied by a good story, a test can only be satisfied by a good fix —
is the whole reason this module exists.

[Ask the room] Has anyone here had an agent tell you with total confidence
that it fixed something, and it hadn't? [Pause for responses.] That
confidence is the failure mode we're targeting today.

### Slide 5 — Quick Refresher: Red / Green / Refactor

Quick refresher for anyone who needs it, and a level-set for everyone else,
because we're going to use this exact vocabulary all session.

Red: you write a test for behavior that doesn't exist yet, and you watch
it fail. Not "you assume it would fail" — you actually run it and watch
the failure. This step proves the test is wired up correctly and is
actually exercising the thing you think it's exercising.

Green: you write the *minimum* code needed to pass that test. Not the most
elegant code, not the most general code — the minimum. Resist the urge to
over-build here; that's what the next step is for.

Refactor: now that you have a passing test protecting you, you clean up
the implementation. Extract constants, rename things, remove duplication —
whatever makes the code better, while the test stays green the entire
time.

And then you repeat, one small increment at a time. That cycle — red,
green, refactor, repeat — is decades old and nothing about agents changes
the cycle itself. What changes is *who's turning the crank*, and that's
our next slide.

### Slide 6 — The Loop, With an Agent Driving

Here's the same loop, but now written as a six-step protocol for when the
agent is the one doing the work.

One: the agent writes a failing test. Two — and read this one carefully,
because it's in bold on the slide for a reason — you, or your CI system,
confirm it fails, *and that it fails for the right reason*. Three: the
agent implements the fix. Four: the agent, or you, confirms the suite is
green. Five: the agent refactors. Six: repeat.

Steps one, three, four, five look almost identical to the human loop. Step
two is where everything hinges, and I want to be very direct with you:
step two is the step humans skip when they're moving fast, and agents skip
it *harder*, because an agent has no discomfort about skipping steps. A
human who skips "confirm the test fails for the right reason" usually has
some background unease about it — a little voice saying "I should really
check that." An agent doesn't have that little voice unless you build it
into the process. It will happily report "test written, now implementing
the fix" without ever having executed the test at all, or having executed
it and gotten a completely unrelated error.

So step two isn't a nice-to-have in this list. It is the entire value
proposition of doing TDD with an agent instead of just asking the agent to
"fix the bug." We're going to spend the next several slides making that
concrete with a real bug, so you can see exactly what step two looks like
in practice and exactly what it catches.

---

## Section: Worked Example — The Bulk-Discount Bug (Slides 7–11) — ~25 min

### Slide 7 — Meet the Bug: A Bulk-Discount Off-by-One

Here's our case study for the rest of the lecture portion. A support
ticket comes in. It says, quote: "Customers say buying exactly 10 units
doesn't get the bulk discount applied. 11 units works fine."

That's it. That's the entire bug report we're going to hand the agent. No
file names. No stack trace. No line number. No "I think the problem is in
the pricing module." Nothing. This is deliberate, and it mirrors the lab
you'll do later today — realistic bug reports from actual users almost
never come with a diagnosis attached. They come with a symptom.

I want you to sit with how little information that is. If you told a
junior engineer "fix this" with just that sentence, they'd go find the
discount logic, poke at it, probably add a print statement, and eventually
figure out it's a boundary condition. An agent can do the equivalent of
all of that — but the question we're asking today is: what's the *first*
thing it should produce? Not a fix. A test.

### Slide 8 — Step 1: Write the Failing Test

The first thing that happens — before anyone touches the pricing function —
is the agent writes this:

```python
def test_bulk_discount_applies_at_exactly_10_items():
    total = calculate_discount(quantity=10, unit_price=5.00)
    assert total == 45.00  # 10 * 5.00 * 0.9
```

Walk through what this does. It takes the vague bug report — "10 doesn't
work, 11 does" — and turns it into one concrete, checkable claim: if you
buy exactly 10 units at $5.00 each, the discounted total should be $45.00,
which is 10 times 5 times 0.9, a 10% discount applied.

That's the whole translation step. Prose becomes an assertion. And notice
the comment on that assert line — it's not decoration, it's showing its
work, which matters both for the human reviewing this test and, frankly,
for the agent itself when it re-reads its own test later in the
conversation.

Now here's the part that's easy to rush past: you run this test *now*,
before touching any implementation code. Not after writing the fix — now,
immediately, while you're confident it should fail. Why does that order
matter? Because it's the only point in the whole process where you get to
verify the test is actually testing something. If you write the test and
the fix in the same breath and then run everything together, and it
passes, you have learned nothing about whether the test would have caught
the bug in the first place.

### Slide 9 — Step 2: Confirm It Fails for the *Right* Reason

So the agent runs the test. Here's what a good failure looks like:

```
AssertionError: 50.0 != 45.00
```

Let's unpack why this is a *good* failure. The test ran to completion. It
executed `calculate_discount`, got an actual number back — 50.0 — and
that number is exactly what you'd expect if the discount weren't being
applied at all: 10 times 5.00, no 10% off. The assertion then correctly
flagged that 50.0 doesn't equal the 45.00 we expected. This failure is
telling us precisely what the bug report told us: the discount math is
wrong, exactly as reported. Good failure.

Now, what does a *bad* failure look like? A `NameError` because the
function was misspelled. An `ImportError` because the test imports from
the wrong module path. A broken fixture that blows up before the
assertion is even reached. These are red flags, and here's the critical
distinction: in every one of these cases, the *test* is wrong, not the
code under test. If you don't look closely at the failure message, all of
these look the same from a distance — "test failed, good, that's red like
we wanted." But they mean completely different things.

This is the single most important habit in this whole module, so let me
say it as directly as I can: skipping this check — actually reading the
failure message and confirming it says what you think it says — is how
agents "fix" typos in a test file and call the bug resolved. The agent
writes a test with a typo, runs it, sees red, "fixes" the typo, sees
green, and reports "bug fixed" — having never touched the actual pricing
logic at all. The bug report is still true in production. Nobody
discovers this until the same support ticket comes back in three weeks,
except now everyone thinks it was already fixed once, which makes the
second investigation slower and more confused than the first.

[Ask the room] Has anyone seen an agent do exactly this — declare victory
after fixing something in the test rather than the code? [Pause.] This is
extremely common, and it's *invisible* if you only glance at pass/fail and
never read the message.

### Slide 10 — Step 3: Implement the Fix, Confirm Green

Now — and only now — the agent is allowed to touch the implementation.
Here's the fix:

```diff
- if quantity > 10:
+ if quantity >= 10:
      total *= 0.9
```

One character. `>` becomes `>=`. That's the entire bug — a classic
off-by-one, a boundary condition that excluded the boundary itself. The
original code said "more than 10 gets the discount," which technically
matches a sloppy reading of "bulk discount for orders of 10 or more," but
excludes exactly the case the bug report is about.

Two things happen next, and both matter. First, re-run the new test — it
should now pass. Second — and this is the step people are tempted to skip
because "the fix was so small" — re-run the *whole* suite, not just the
new test. A one-character change to a boundary condition is exactly the
kind of edit that can silently break an adjacent case. Maybe there's
another code path that relied on the old, technically-wrong behavior.
You don't know until you run everything.

Only after both of those come back green does the agent touch anything
else. Notice what we have *not* done yet: we haven't cleaned anything up.
The threshold is still a bare literal `10` in an `if` statement, the
discount rate is still a bare `0.9`. That's fine — green is green. The
next step is where that gets addressed, and it's the step almost everyone,
human or agent, is tempted to skip.

### Slide 11 — Step 4: Refactor (the Step Agents Skip)

Here's the refactor:

```python
BULK_DISCOUNT_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.9

if quantity >= BULK_DISCOUNT_THRESHOLD:
    total *= BULK_DISCOUNT_RATE
```

We've pulled the magic numbers out into named constants. Nothing about
behavior changed — the test suite should still be green before and after
this edit — but now the next person who reads this code, human or agent,
can see at a glance what "10" and "0.9" actually mean, and if the
business changes the threshold to 15 units next quarter, there's one
place to change it instead of a literal buried in a conditional.

Here's the point I really want to land: green tests *feel* like "done" to
an agent. There is no test in the suite that says "these should be named
constants" — nothing is red, nothing is demanding this cleanup happen. So
if you don't explicitly ask for it, it usually doesn't happen. The agent
will report the bug fixed, the tests passing, and stop, because from a
pure test-runner perspective, it *is* done.

This is worth generalizing beyond this one example: green tests are a
safety net *for* cleanup, not a reason to skip cleanup. The whole point of
having a passing suite is that it gives you the confidence to refactor
aggressively, because you'll know immediately if you break something. If
you have the safety net and never use it, you're leaving value on the
table. In practice, this means: after the agent reports green, explicitly
ask "now refactor this, keeping the tests green" as its own instruction.
Don't assume it's implied.

[Transition] So that's the whole loop, worked end to end on a real bug.
Now let's zoom out and talk about the tests themselves — specifically,
two different philosophies for what a test-as-spec should look like.

---

## Section: Example-Based vs. Property-Based Tests (Slides 12–15) — ~25 min

### Slide 12 — Example-Based Tests as a Spec

The test we just wrote — quantity equals 10, expect 45.00 — is an
example-based test. It's one of a family that would typically look like
this:

```python
def test_bulk_discount_applies_at_exactly_10_items(): ...
def test_no_discount_at_9_items(): ...
def test_discount_on_a_large_order(): ...
```

Each one picks a specific input and asserts a specific expected output.
These are precise, they're readable — anyone on the team can look at the
test name and the assertion and understand exactly what behavior is being
locked in — and they're cheap for an agent to write, because going from
"here's a bug report with a specific number in it" to "here's a test with
that specific number in it" is a very short, very mechanical hop.

But here's the limitation, and it's an important one for working with
agents specifically: an example-based test is only as good as the examples
someone thought to write. If nobody thinks to test 0 units, or a
fractional unit price, or a quantity of 10,000, those cases simply aren't
covered, full stop.

And here's the sharper version of that problem when an *agent* is the one
writing the examples: an agent will happily write examples that confirm
its *own* assumption about where the boundary is. If the agent's mental
model of the fix is "discount kicks in at 10," it will write a test for 10
and a test for 9, and both will pass, and it will feel thorough — because
it wrote multiple tests! — while never probing whether the boundary is
actually correct, or whether some other edge, like negative quantities or
enormous orders, breaks the same function in a different way. The tests
it writes are shaped by the same mental model that might contain the very
mistake you're trying to catch. That's a blind spot that doesn't announce
itself.

### Slide 13 — Property-Based Tests as a Spec

This is where property-based testing comes in, and if this is new to
some of you, here's the core idea. Instead of picking specific inputs and
specific expected outputs, you state an invariant — a property that must
hold true for *all* valid inputs, not just the ones you thought of.

A generator — a piece of the testing library — then produces hundreds of
randomized cases automatically, including combinations nobody sat down
and thought to write by hand. If the invariant fails for any of those
generated cases, the test fails, and the library will typically also
"shrink" the failing case down to the smallest example that still
reproduces the failure, which is enormously useful for debugging.

For our discount function, what's the invariant? Something like: the
discounted total should never exceed the full, undiscounted price. That's
a statement that should be true no matter what quantity or unit price you
plug in — it's not about the number 10 specifically, it's a structural
truth about what a discount even *means*. A discount that makes you pay
more than full price isn't a discount, it's a bug, regardless of which
quantity triggers it.

Notice the shift in who's responsible for what. With example-based tests,
you're responsible for picking good example inputs. With property-based
tests, you're responsible for correctly identifying the invariant — and
then the machine handles generating the inputs. That's a different kind
of work, and it plays to different strengths.

### Slide 14 — Worked Example: A Property-Based Test

Let's make that concrete with actual code, using Hypothesis, a popular
Python property-testing library:

```python
from hypothesis import given, strategies as st

@given(
    quantity=st.integers(min_value=0, max_value=10_000),
    unit_price=st.floats(min_value=0.01, max_value=10_000),
)
def test_discount_never_exceeds_full_price(quantity, unit_price):
    assert calculate_discount(quantity, unit_price) <= quantity * unit_price
```

Read this with me. The `@given` decorator says: generate `quantity` as
integers between 0 and 10,000, and `unit_price` as floats between one
cent and 10,000. Hypothesis will then call this test function hundreds of
times with different combinations drawn from those ranges, and every
single time, it checks that the discounted result is less than or equal
to the full undiscounted price.

What does this catch that our example-based tests never touched? Three
things worth calling out explicitly. First, `quantity=0` — did anyone
write an example test for buying zero units? Probably not; it's not what
the bug report was about, so it's easy to never think of it. Second,
genuinely huge orders — quantity in the thousands, at a high unit price —
which might expose overflow or scaling issues that never show up at
"normal" quantities. Third, and this one's subtle: floating-point
rounding. It's entirely possible for a rounding error in the discount
math to push the "discounted" total *above* the full price by a fraction
of a cent for some specific combination of inputs — something you would
almost never stumble onto by picking round numbers like 10 and 5.00 by
hand, but that a generator sweeping through hundreds of floats will find
eventually.

This is the payoff of property-based testing: it's not smarter than you,
it's just tireless in a way that's genuinely hard for a human — or an
agent working from a single bug report — to replicate by hand.

### Slide 15 — Choosing, With an Agent Driving

So which do you use? Here's the comparison as a table, and I want to walk
through each row because the "with an agent driving" framing changes the
calculus a bit from how you might reason about this if you were coding
solo.

Best for: example-based is best for reproducing the bug report's exact
scenario — it's a direct translation of the complaint into code.
Property-based is best for boundary and invariant coverage — catching the
things the bug report didn't mention because the reporter never
encountered them.

Who writes it, and how easily: an agent can write an example-based test
fast, straight from the report, because the translation is nearly
mechanical. A property-based test needs an invariant, and — this is the
key asymmetry — that invariant has to be stated by *you*. An agent can
help you phrase it once you've identified it, but identifying "the
discounted total should never exceed full price" as the right invariant
requires understanding what the function is *for*, not just what it
currently does. That's a judgment call, and right now, that judgment call
belongs to the human in the loop.

Main risk of each: example-based tests are narrow — they only test what
somebody imagined, and an agent's imagination is anchored to the bug
report it was handed. Property-based tests are only as good as the
invariant — if you state a weak or trivially-true invariant, the
generator will run hundreds of cases against something that doesn't
actually constrain the bug, and you'll get a false sense of security from
a big green checkmark.

The practical guidance, and the one I want you to take into the lab:
use example-based tests to reproduce the bug — that's your red step, it's
fast, and it directly encodes what was reported. Then *add* a
property-based test to check that the fix is actually general, not just
shaped exactly like the bug report. The two are complementary, not
competing — you're not choosing one methodology forever, you're reaching
for the right one at the right moment in the same fix.

---

## Section: Hallucination & Failure Modes (Slides 16–18) — ~15 min

### Slide 16 — Why Failing Tests Reduce Agent Hallucination

Let's come back to the conceptual core of the module, now that you've
seen the mechanics in detail. Why, specifically, do failing tests reduce
hallucination?

Start with what hallucination looks like in this context. It's not the
agent inventing a fake API — that's the more commonly discussed kind.
Here, hallucination looks like confident overclaiming: "I've fixed the
bulk discount issue" when nothing was actually verified to work. A prose
bug report is ambiguous by nature — it describes a symptom, not a
mechanism — and an agent, like a person under pressure to seem helpful,
will fill the gaps in that ambiguity with a guess, and then present that
guess with the same confident tone it uses for things it's actually
verified. There's no tell. The sentence "I've fixed the bug" reads
identically whether it's true or not.

A failing test breaks that symmetry. It's a checkable contract: the fix
is either green or it isn't, and that's a fact about the world you can
check yourself in about two seconds, independent of how the agent
describes what it did. No persuasive explanation, no amount of confident
prose, substitutes for the test actually passing. You don't have to
evaluate the *quality of the argument* the agent makes — you just run the
suite.

And here's the deeper mechanism: a failing test forces the agent to
*run* something instead of *asserting* that something worked. Those are
fundamentally different actions. Asserting is free — language models are
extremely good at producing fluent, confident assertions regardless of
their truth value, because that's what the training process optimizes
for: plausible next tokens. Running a test and reporting its actual
output is not free in the same way — it's the agent producing a
transcript of something that either did or did not happen in the world,
and that transcript is something you, the human, can independently check.
The entire discipline of TDD-with-agents is about maximizing how often
you make the agent do the second thing instead of the first.

### Slide 17 — Failure Mode: The Test That Passes for the Wrong Reason

But I'd be doing you a disservice if I made it sound like "just use
tests" is a silver bullet, because tests themselves can be hallucinated
too, in a specific and important way. Here's the extreme, almost comedic
version:

```python
def test_bulk_discount():
    assert True  # "verified manually"
```

Nobody's proud of writing that, and most agents won't write anything
quite this blatant. But I put it on the slide because the pattern behind
it is completely real, just usually dressed up more subtly. The
realistic versions look like: over-mocking, where the mock is configured
to already return the expected value, so the test verifies that the mock
does what you told it to do rather than that the code does what it's
supposed to do. Or asserting on a constant that has nothing to do with
the actual computed result. Or, more insidiously, testing the mock
instead of the code — patching out the exact function under test and then
asserting something about the patch.

The fix — and this connects directly back to Slide 9 and step two of the
loop — is: read the failing test's *error message* before you ever trust
the green one. If you never watched this test fail, and fail for a
reason that makes sense to you, you have no basis for trusting that its
later "pass" means anything. A test that has never meaningfully failed is
a test you haven't actually verified is testing anything at all.

### Slide 18 — Where This Pairs Well — and Poorly

So, given everything we've just walked through — where should you
actually reach for this technique, and where should you not?

It pairs well with bug fixes, well-defined logic, pure functions, parsers,
calculations — anywhere "correct" is already knowable in advance,
independent of the fix itself. Our discount example is a perfect fit:
there's a formula, there's a right answer, and you can state that answer
as an assertion before any code changes.

It pairs poorly with exploratory UI work, or anything in the category of
"make it feel right." Think about trying to TDD your way to a good-feeling
animation timing, or a color palette, or the wording of an error message
that should feel reassuring rather than alarming. If you tried to write
the test first here, you'd be writing assertions about an answer you
don't actually have yet — you'd be guessing at what "correct" even means
before you've explored the problem, which inverts the entire value
proposition of the technique.

So here's the honest caveat I want you to sit with: TDD-with-agents
assumes the test is right *before* you write it. That's a real
assumption, not a given. It's easy to internalize "tests are ground
truth" so thoroughly that you forget the test itself is an artifact
someone — you, or the agent under your direction — wrote, and it can
encode the wrong thing just as easily as a prose spec can. The technique
doesn't remove the need for judgment; it relocates where the judgment
gets applied — to writing a correct assertion up front, rather than
reviewing a diff after the fact.

---

## Section: Lab & Wrap-Up (Slides 19–22) — ~15 min

### Slide 19 — Lab: Bug Report Only

Now it's your turn. Here's the lab.

You will hand your agent **only** a bug report. No file names, no hints,
no suspected cause — same constraint we put on ourselves in the worked
example. Pick a real or realistic bug in the codebase you're working with
today, and write the report the way a support ticket or a confused user
actually would: describe the symptom, not the mechanism.

The required sequence, and I want this followed exactly, not
approximately: one, write a test that reproduces the bug and fails. Two,
confirm the failure is for the right reason — read the actual message,
don't just glance at red versus green. Three, implement the fix. Four,
confirm the test passes and that nothing else broke, meaning the whole
suite, not just your new test.

If you find yourself tempted to let the agent write the test and the fix
in the same turn without stopping to look at the failure in between —
resist that. That's the exact shortcut this whole module has been about
not taking.

### Slide 20 — Lab Walkthrough — What "Done" Looks Like

Before you dive in, let's be precise about what a completed lab exercise
actually looks like, because "I fixed the bug" is not a sufficient bar
today.

You need two separate commits: one containing the failing test, and one
containing the fix. Never squashed together. This isn't bureaucratic
box-checking — it's the artifact that proves the loop actually happened
in the right order, rather than being reconstructed after the fact to
look tidy.

Here's a concrete check you can run on yourself: the failing-test commit's
diff should contain no production code changes whatsoever — if it does,
that's a sign the test and the fix got written together and you skipped
the moment where you'd have caught a bad test.

And before you consider merging anything, do this: re-read the assertion
in your test, cold, as if you'd never seen it before, and ask — does this
actually encode the bug report, or does it encode something merely
adjacent to it? This is the human judgment step that no amount of process
substitutes for. It's entirely possible to follow every step of this loop
correctly and still end up with a test that's slightly off-target from
what was actually reported. Catching that is on you.

### Slide 21 — Deliverable

Your deliverable has two parts. First, the two commits themselves —
failing test, then fix, kept separate in history, exactly as we just
discussed.

Second — and don't skip this part, it's short but it's the part I
actually care about most — a one-line note: did the agent's *first*
attempt at writing the test actually capture the bug correctly, or did it
need correction from you?

Here's why that one line matters more than it looks like it should. That
note is the real signal. It's not about this one bug — it's calibration
data about how much you can trust this agent's *next* test, when you're
not standing over its shoulder watching every step. If the first attempt
nailed it, that's evidence you can extend a bit more autonomy next time.
If it needed correction — if the agent's test conflated two different
symptoms, or missed the actual boundary condition, or tested something
adjacent to the real bug — that's evidence you should keep reviewing this
category of test closely for a while longer. You're not just fixing a
bug today; you're building a track record of one specific agent's
reliability on one specific kind of task, and that track record is what
lets you eventually work faster with confidence instead of blind faith.

### Slide 22 — Recap & Next Module

Let's close the loop on today. Tests as an executable spec close off the
room an agent has to guess — that's the throughline for everything we
covered. Red, green, refactor — and specifically, "confirm it fails for
the right reason" — is the step that actually matters; everything else in
the loop is close to what you'd expect from ordinary TDD, but that one
step is the part that's genuinely different when an agent is doing the
driving. Example-based tests to reproduce a specific reported bug,
property-based tests to check that your fix generalizes beyond the exact
shape of that report — use both, at different moments, in the same fix.

Next time, in Module 7, we're going in the opposite direction: what
happens with no upfront doc and no test at all — conversational,
iterative development, where the spec isn't written down anywhere before
you start talking to the agent. You'll see very quickly why today's
lesson makes that mode either safer or considerably riskier, depending on
how disciplined you are about applying it. See you then.

[End of lecture. Transition to lab time.]
