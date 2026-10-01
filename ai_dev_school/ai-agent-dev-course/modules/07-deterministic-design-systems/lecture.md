# Module 7 — Lecture Script: Deterministic Design Systems for AI-Generated UI

This is the full spoken script for the live session, matched slide-by-slide
to `slides.md`. Timing notes are approximate and assume roughly 60–75
minutes of lecture followed by a lab of about an hour to an hour and a
half — long enough to actually run three separate agent sessions and
compare screenshots, which is what this module's lab requires. Adjust to
your cohort's pace; the numbers are a planning aid, not a contract.

---

## Section 1 — Framing the Problem (Slides 1–5) — ~20 min

### Slide 1 — Module 7: Deterministic Design Systems for AI-Generated UI

Welcome back. Over the last few modules we've been building a discipline
around agentic development that all points the same direction: don't let
the important decisions live only inside a conversation, because a
conversation doesn't persist and doesn't transfer. Module 6 did this for
*behavior* — that was the whole point of DDD, deterministic-driven
development: specs and plans instead of "the agent remembers what we
discussed an hour ago." Today we're doing the exact same move, but aimed
at something that feels much softer and harder to pin down: what your UI
actually looks like.

The case-study focus for today is tokens plus design docs for reproducible
UI. That phrase — reproducible UI — is doing a lot of work, and I want you
to sit with it for a second, because "reproducible" is not a word most
people naturally associate with design. Design feels like the creative,
subjective part of building software, the part where you'd expect some
variation session to session. By the end of today, I want you to see that
variation not as an inevitable cost of creativity, but as a symptom of a
missing artifact — exactly the same diagnosis we made about behavioral
drift back in Module 6.

### Slide 2 — Agenda

Here's the shape of today. We'll start with why this module exists at
all — the actual mechanism behind why an agent's UI output drifts from
session to session, even when you feel like you're asking for the same
thing. Then we'll walk through five concepts in sequence, and I want you
to notice that they build on each other rather than being five
independent tips: design tokens, which give you concrete values instead of
prose; a design system doc, which carries the rationale tokens can't
express on their own; a repo-level rule that actually forces an agent to
look at both; packaging repeated design work as a Skill, which takes
enforcement even further; and closing the loop with visual review, because
a clean diff can still render wrong. After that we'll set up today's lab —
three sessions, one small UI, and a very deliberate comparison — and close
with the deliverable and some discussion questions worth sitting with
after class.

### Slide 3 — Why this module exists

Let's start with the actual mechanism, because "AI is inconsistent with
design" is too vague a complaint to build a fix around — it's exactly the
kind of vague adjective we're about to spend the whole lecture arguing
against, so let's not lead with one.

Here's the precise claim: an agent session has no memory of *why* it
picked a given blue, or a given spacing scale, or a given font, the last
time it built something for you. Not "chooses inconsistently" — has no
memory of the choice at all. If you started a session yesterday and it
landed on `#4f46e5` for your primary accent color, and you start a
completely fresh session today and ask for the same kind of page, that
fresh session isn't recalling yesterday's blue and deciding whether to
reuse it. It's starting from zero and deriving an accent color from
scratch, from whatever adjectives happened to be in today's prompt.

This is the same failure Module 6 diagnosed for behavior, and I want to
draw the parallel explicitly because it's not just a rhetorical
similarity — it's the identical root cause. In Module 6, the problem was:
if "the plan" only exists as a conversation, every new session re-derives
requirements from scratch, and small differences in how you phrase the ask
produce small differences in what gets built. Today: if "the design" only
exists as a conversation, every new session re-derives the palette,
spacing, and typography from vague adjectives — "modern," "clean" — and
produces a visibly different result each time. Same mechanism, different
surface. And the fix has the same shape too: determinism comes from moving
decisions out of the conversation and into files the agent reads fresh
every session. It is not a prompting trick. You cannot phrase your way out
of this problem, because the problem isn't that your prompt was unclear —
it's that certain kinds of instructions structurally don't have one fixed
answer, which is exactly what the next slide is about.

### Slide 4 — Learning objectives

Three things I want you walking out of today's session able to do.

One: externalize design decisions into artifacts an agent reads *before*
generating any UI. Not "have good taste" or "give better prompts" — build
a file, or a small set of files, that sits in the repo and gets consulted
before any styling work happens. This is an infrastructure change, not a
communication-skill change.

Two: understand why concrete values — hex codes, a numeric spacing scale,
a named font stack — are what actually buys you determinism, while
descriptive language is exactly where the drift creeps back in. This one
matters because it's tempting to think a *really good* design doc written
in careful, precise prose would solve the problem. It won't, not fully,
and by the end of the tokens section you'll see exactly why.

Three: close the loop with visual verification instead of trusting a
text-only diff to catch design drift. This is the one people skip, because
it feels like extra work, and it's also the one that catches an entire
category of bug the other four concepts can't touch on their own. We'll
get to why near the end.

### Slide 5 — The core problem: "modern and clean"

Let's make the drift concrete, because until you've actually seen it
happen it's easy to assume it's theoretical.

Picture two engineers on your team, in two different agent sessions, both
building pages for the same product. Both give essentially the same
prompt: "build a settings page, keep it modern and clean, consistent with
the rest of the site." Session A's agent picks `#4f46e5` for the primary
button color. Session B's agent, given what is functionally the same
prompt, picks `#4338ca`. Go look at those two hex codes side by side —
they're both perfectly reasonable, professional-looking indigos. Neither
one is a mistake. If you showed either color to a designer in isolation
and asked "does this look modern and clean?", they'd say yes without
hesitation.

The problem isn't that one of them is wrong. The problem is that they
don't *match*. Put those two buttons on two pages of the same product and
a user notices immediately, even if they can't articulate why — it just
feels like two different apps stitched together. And here's the part I
really want to land: this is not a communication failure that better
prompt engineering fixes. "Modern," "clean," "professional" are not
underspecified in the sense that a more careful writer could nail them
down with enough extra adjectives. They're underspecified in a much more
fundamental sense — they're a category of instruction that has no single
fixed answer. There is no canonical "modern blue." There's a wide space of
colors that satisfy that description, and every time you ask an agent —
or a human designer working from a one-line brief, for that matter — to
pick a specific point in that space, you're implicitly asking it to make a
decision that the prompt didn't actually make for it. Two independent
agents, or two independent humans, making that same implicit decision
independently will not reliably converge. That's not a bug in the model.
That's what "underspecified" *means*.

So if the fix isn't a better prompt, what is it? Move the decision out of
the adjective and into a value that gets made exactly once, written down,
and reused. That's the entire idea behind design tokens, and it's where we
turn next.

---

## Section 2 — Key Concept 1: Design Tokens (Slides 6–8) — ~15 min

### Slide 6 — Key concept 1: Design tokens — values, not prose

Here's the fix in its simplest form: a real `tokens.css` or `tokens.json`
file — or the equivalent in whatever styling system your stack uses — that
the actual code *imports*. Not a document that describes the palette in
words. A file the build actually consumes.

```css
:root {
  --color-bg: #0b0d10;
  --color-accent: #6ee7ff;
  --font-heading: "Inter", system-ui, sans-serif;
  --space-unit: 8px;
  --radius-base: 6px;
}
```

Look at what's on that list: a background color as a literal hex value, an
accent color as a literal hex value, a heading font as a literal named
stack, a spacing unit as a literal pixel value, a corner radius as a
literal pixel value. None of these is a description. None of these leaves
room for interpretation. "The accent color is `#6ee7ff`" is not a
statement that two different readers — human or agent — can reasonably
disagree about. That's the entire trick, and it really is that simple to
state. The hard part isn't the concept; it's actually doing it instead of
reaching for a paragraph of adjectives because a paragraph feels more
thorough.

### Slide 7 — Tokens: what makes this different from a style guide PDF

I want to spend real time distinguishing this from something that looks
superficially similar, because a lot of teams already have a "brand
guidelines PDF" sitting somewhere, and they assume that's the same thing.
It is not, and the difference is the whole mechanism.

First: every value in a tokens file is machine-consumable, and the actual
code references it directly — `color: var(--color-accent)`, not "use the
brand blue from page 12 of the style guide." There's no human, or agent,
standing between the token and the rendered pixel, translating a
description into a value. That translation step is exactly where drift
gets introduced, because translation always involves a judgment call, and
judgment calls made independently by different sessions don't converge.

Second: a spacing *scale* beats ad hoc margins. Instead of one component
using `margin: 14px` and another using `margin: 16px` because two
different sessions each eyeballed "about right," you define
`--space-unit: 8px` once, and then every spacing value in the entire UI is
a multiple of it — 1x, 2x, 3x, 4x. This does two things at once: it gives
you visual rhythm, because consistent multiples of a base unit read as
intentional in a way arbitrary pixel values don't, and it gives you a
single place to adjust the whole system's density if you ever need to.

Third, and this is the point that actually matters most for our purposes:
one file is one source of truth. Not "the palette we agreed on three weeks
ago in a Slack thread that's since scrolled off," not "whatever the
designer's Figma file currently says, assuming it's been kept in sync with
the code" — one file, in the repo, versioned alongside the code it
styles. A PDF style guide can go stale the moment someone changes a color
in the actual product without updating the PDF. A tokens file *can't* go
stale in that way, because the tokens file is what produces the color.
There's nothing else for it to drift out of sync with.

### Slide 8 — Why tokens structurally prevent drift

Now let's get to the mechanism that actually makes this work, because I
don't want you to walk away thinking tokens are just "good practice" in
some vague, hand-wavy sense — the enforcement here is structural, and
that's a specific, checkable claim.

To introduce a new color anywhere in the UI, the agent has to edit
`tokens.css`. Think about what that means concretely: adding a color is no
longer a silent, local decision buried inside one component's styling.
It's an edit to a shared file, and that edit shows up in the diff. A
human reviewing the pull request sees a new custom property appear. A
review agent, if you're running one — recall Module 5's implementer and
reviewer patterns — sees it too. Either way, the decision to introduce a
new color has been made *visible* and *reviewable*, purely as a side
effect of where the token lives.

Now compare that to the alternative: a color baked directly into a
component's inline style, or a one-off `style={{color: '#4338ca'}}`
sitting inside some JSX thirty lines deep in a file nobody's looking at
closely. That color is completely invisible in review. Nobody reading the
diff line by line is going to clock a hex code as "wait, is this actually
one of our approved colors?" unless they happen to have the whole palette
memorized. It becomes visible only when you're staring at two rendered
screenshots side by side and something feels subtly off — which is far
too late, and far too expensive a way to catch it.

So here's the sentence I want you to hold onto for the rest of the module,
because it reframes everything that follows: determinism here isn't about
a smarter model. It's not that a more capable agent would somehow "know
better" and reuse the same blue. It's about removing the decision from the
conversation entirely. The agent isn't being asked to remember or infer
the right color anymore — it's being asked to *look one up*, and looking
up a value from a file is a task models are extremely reliable at,
precisely because it doesn't require judgment. We've converted a judgment
call into a lookup. That conversion is the whole game.

---

## Section 3 — Key Concept 2: The Design System Doc (Slides 9–10) — ~10 min

### Slide 9 — Key concept 2: Design system doc — patterns and rationale

Tokens solve "what color." They don't solve "when do we use it, and why."
For that you need a second artifact, and I want to be very precise about
its scope up front, because the biggest way teams get this wrong is
letting it balloon: a short doc, one page, not a brand book.

What goes on that one page: the layout grid and breakpoints — how many
columns, where the page reflows. Component states — hover, active,
disabled, error — because a static screenshot of a button doesn't tell you
what it looks like mid-interaction, and that's exactly the kind of detail
that gets improvised differently session to session if it's not written
down. Tone and voice, briefly. And one or two reference sites — literally,
"look like this, not like that" — because sometimes the fastest way to
communicate a design direction is a concrete example to anchor against,
the same way a spec in Module 6 might point at an existing feature as a
behavioral reference rather than describing every edge case in prose.

The relationship between this doc and the tokens file is worth stating
explicitly, because it's easy to conflate them: tokens say *what* — this
is the exact accent color, this is the exact spacing unit. The doc says
*why and how they combine* — cards get a border in this token, but only a
shadow on hover; the primary action always uses the accent color, and
there's only ever one of them per screen. That second kind of statement
isn't a value you can put in a CSS custom property. It's a rule about
*usage*, and usage rules are exactly what a one-page doc is for.

### Slide 10 — What belongs in the doc (and what doesn't)

Let's get concrete about the boundary, because "keep it short" is itself
a vague adjective if I don't show you where the line actually falls.

In: "Cards use `--radius-base`, a 1px border in `--color-border`, and a
shadow only on hover." Notice what that sentence is doing — it references
tokens by name rather than restating their values, and it encodes a
*rule* about combination and state that the tokens file has no way to
express on its own. Another example: "Primary actions are always
`--color-accent`; never more than one per screen." Again — that's not a
value, it's a constraint on how values get used, and it's exactly the
kind of thing an agent building a new page needs to know to avoid putting
three equally-loud accent-colored buttons on one screen because nothing
told it not to.

Out: a restatement of the tokens file. If your design doc has a section
that says "our colors are: background `#0b0d10`, accent `#6ee7ff`..." —
delete it. That's not documentation, that's a second copy of the same
fact sitting in a place that won't get updated when the first copy
changes, which means it will go stale, which means you've reintroduced
exactly the "which version is current" problem tokens were supposed to
eliminate. Also out: full brand mythology, logo-usage rules, marketing
copy guidelines. Not because those things are unimportant in some
absolute sense — a company might genuinely need logo-usage guidelines for
legal or brand reasons — but because none of it helps an agent generate a
settings page correctly, and every extra page of unrelated content is a
page competing for attention with the two or three facts that actually
matter for this task. The discipline here is the same discipline as a
good spec in Module 6: say what's needed to build the thing correctly,
and stop.

---

## Section 4 — Key Concept 3: The Repo-Level Rule (Slides 11–12) — ~10 min

### Slide 11 — Key concept 3: A repo-level rule that forces the check

Here's a fact that trips people up the first time they build a tokens file
and a design doc and then watch an agent completely ignore both: neither
artifact helps if the agent doesn't know to look for it. A file sitting
in `design/tokens.css` does nothing on its own. An agent has to be told,
explicitly, that it exists and that it must be consulted — this cannot be
an assumption, the same way you wouldn't assume a new engineer on your
team would somehow intuit that a style guide exists without anyone
mentioning it to them.

So the third artifact is a rule, and it goes in the one place we already
know gets read at the start of every session — `CLAUDE.md` or `AGENTS.md`,
the same file where Module 1 had you put project-level instructions:

```md
## Design
Before any UI/styling work, read design/tokens.css and
design/system.md. Do not introduce new colors, fonts, or
spacing values outside the tokens file — extend the tokens
file instead and use the new token.
```

Notice the shape of that instruction. It's not "try to be consistent with
our design." It's a concrete, imperative sequence: read these two specific
files, before this specific category of work, and — this is the part that
closes the loop back to Slide 8 — if you need something new, the
mechanism for adding it is spelled out too: extend the tokens file, don't
improvise around it. That last clause matters enormously in practice,
because without it, an agent that needs a color not currently in the
palette has exactly one path available: invent one inline and move on.
Giving it an explicit, sanctioned path — "add it to the tokens file" —
means the inevitable case of "we need something not yet defined" still
goes through the reviewable, diffable mechanism from Slide 8 instead of
around it.

### Slide 12 — Why you need all three, not just one

Let's stress-test this by looking at what happens when you have only one
of the three artifacts, because seeing each failure mode individually is
what makes the "you need all three" claim land as something more than an
assertion.

Tokens, no rule: the agent never opens the file, because nothing told it
to, and it invents new hex codes anyway, exactly as if the tokens file
didn't exist. The artifact was perfect. It just sat there unread.

Doc, no tokens: you write a beautiful one-page doc that says "use a calm,
professional blue for primary actions." That sentence is still an
adjective in disguise — "calm" and "professional" are exactly as
underspecified as "modern and clean" was back on Slide 5, just moved into
a nicer-looking document. A doc without concrete values doesn't buy you
determinism no matter how well-written it is, because the underlying
problem was never about writing quality.

Rule, no artifacts: the agent dutifully does what the rule says — it goes
and reads `design/tokens.css` and `design/system.md` — and finds nothing
there, or finds stub files nobody ever filled in. It followed the
instruction perfectly and there was nothing to enforce.

So here's the relationship, stated plainly: the rule is the *hook*.
Tokens plus doc are what it hooks *into*. A hook with nothing to grab onto
does nothing. Artifacts nobody's told to check don't get checked. You need
the mechanism and the content, together, or the whole thing collapses back
into exactly the drift problem we started with.

---

## Section 5 — Key Concept 4: Packaging as a Skill (Slides 13–14) — ~10 min

### Slide 13 — Key concept 4: Package repeated design work as a Skill

The rule we just built is a real fix, and for a lot of teams it's enough.
But there's a next step worth knowing about, especially once a particular
kind of request stops being occasional and starts being routine.

Here's the trigger condition: if pages or components get built often,
"build a page following our design system" stops being a one-off ask and
becomes a repeatable request — the same shape of task, over and over,
just with different content. When you notice that pattern, it's worth
wrapping it as a Skill — a `SKILL.md` — that *always* loads the tokens
file and the system doc first, before writing any markup at all, as a
built-in step of how the skill executes rather than as an instruction the
agent has to remember to follow.

The shift in what's actually being guaranteed is the important part: we
move from "the agent remembered the `CLAUDE.md` rule this session" to
"the workflow cannot run without it." That's a meaningfully stronger
guarantee, and it's worth being precise about why it's stronger, which is
what the next slide is about.

### Slide 14 — Skill vs. rule: enforcement by construction

A repo rule, even a well-written one, depends on the agent choosing to
follow it in this particular session. Almost always it will — that's why
Slide 11's fix works as well as it does — but "almost always" is a
probabilistic guarantee, resting on the rule being read, parsed, and
acted on correctly every single time, out of everything else in the
context.

A Skill's steps are baked into *how the task gets done at all*. If step
one of the skill's procedure is "read tokens.css and system.md," then
there is no path through executing that skill that skips step one — it's
not competing with other instructions for the agent's attention, it's the
first rung of the ladder the rest of the task is built on. That's the
difference between "please remember to do X" and "X is literally the
first thing that happens, structurally, every time this runs."

If this framing sounds familiar, it should — it's the exact same
relationship as Module 6's spec-plan-implementation loop, just applied to
a narrower, more repeatable job. In Module 6, a spec turns "build
whatever seems reasonable" into "build against this written contract."
Here, a Skill turns "build a page following our design system, and please
remember to check the tokens" into "run this procedure, which starts by
loading the tokens, full stop." Same underlying move: convert a hoped-for
behavior into a structural guarantee.

One practical note on timing, because I don't want you rushing out of
today's lecture to wrap every future UI task in a Skill immediately: this
is a good candidate once you've built the same *kind* of page two or
three times by hand, using the tokens-plus-doc-plus-rule setup from the
last section. Before that point, you don't yet know what the repeatable
shape actually is, and a Skill written too early tends to encode the
quirks of whatever single page you happened to be building when you wrote
it.

---

## Section 6 — Key Concept 5: Visual Verification (Slides 15–16) — ~10 min

### Slide 15 — Key concept 5: Verify visually, not just by reading the diff

Everything so far has been about getting the *inputs* right — tokens, a
doc, a rule, maybe a Skill. This last concept is about checking the
*output*, and it catches a category of bug none of the previous four can
touch.

Here's the failure mode: a code diff can look completely clean — every
color reference goes through a token, nothing hardcoded, the diff reviews
beautifully — and the page can still render wrong. A token gets applied in
the wrong context: maybe `--color-accent` correctly appears in the
stylesheet, but it's applied to a background where the design doc actually
called for it on text only, and now you've got low-contrast text nobody
would have predicted from reading the CSS in isolation. Or a state was
never styled at all: the `:disabled` selector for a button simply doesn't
exist in the new component, so a disabled button renders visually
identical to an enabled one, and nothing about that shows up as a
suspicious line in a text diff — the *absence* of a rule doesn't produce a
diff line to notice.

This is exactly the category of bug that text-only review structurally
cannot catch, for the same underlying reason self-review has a blind
spot in Module 5's implementer/reviewer material: you're checking whether
the code *looks* correct, which is a different question from whether the
*rendered result* is correct, and a diff only ever shows you the former.
So: render the page. Dev server plus a browser preview, or a screenshot if
that's more practical for your workflow — every session, not just when
something feels off. And compare what you're looking at against the
design doc's reference sites and its documented component states, not
just against your general sense of whether it looks fine.

### Slide 16 — Closing the loop

Let's put the whole system together as one picture, because up to now
we've walked through five concepts somewhat linearly, and I want you to
see them as a closed loop rather than a checklist you run through once.

```
tokens.css + system.md  →  repo rule (CLAUDE.md/AGENTS.md)
        │                          │
        └────────► agent generates UI ◄────────┘
                         │
                    render / screenshot
                         │
              compare against design doc
                         │
              gap found? → fix the doc, not just the page
```

Walk it left to right: tokens and the system doc feed into the repo rule,
which is what actually gets the agent to open them before generating
anything. The agent generates the UI. Then — and this is the step Slide
15 just argued is non-negotiable — you render it and look at it, comparing
against the design doc specifically, not just eyeballing it in a vacuum.

Now look at the bottom-left arrow, because it's the one people skip, and
it's the one that actually makes this a *loop* instead of a one-way
pipeline: if you find a gap during that visual comparison — a state that
rendered wrong, a token applied in a context nobody anticipated — the fix
is not just to patch that one page and move on. The fix is to update the
doc, so that the *next* session, building a *different* page, doesn't
independently reproduce the exact same gap. This is precisely the same
discipline as Module 6's spec-correction step: when reality disagrees
with your artifact, the artifact is what's wrong, and you fix the
artifact, not just the one instance of the symptom. A design system doc
that never gets corrected in response to what you actually observe
rendered on screen is a doc that will keep silently missing the same
class of case, session after session.

---

## Section 7 — Lab Setup (Slides 17–18) — ~10 min

### Slide 17 — Lab: three sessions, one UI

Here's what you're building for the rest of this session, and I want to
walk through all five steps before anyone starts, because the value of
this lab depends on doing the steps in this specific order, not jumping
ahead.

Step one: write a tokens file and a one-page design doc for a small
multi-page UI — three to four screens or components is genuinely enough,
you do not need to design an entire product. Step two: add the
`CLAUDE.md`/`AGENTS.md` rule from Slide 11, pointing at both files you
just wrote. Step three — Session A: a fresh session, building using
*only* the tokens, the doc, and the rule — no extra verbal design
guidance beyond describing the feature itself. Resist the urge to also
tell it "and make the buttons rounded" in the prompt; if that matters, it
belongs in the doc, not in today's one-off ask. Step four — Session B: a
completely fresh session with no memory of Session A, building a
*different* page from the same small UI, under the exact same
constraints. Step five — Session C, the control: another fresh session,
the same kind of ask, but this time *without* pointing it at the tokens
file or the doc — just the old, vague "make it look modern and consistent
with the rest of the site."

Notice the structure here mirrors an actual experiment, on purpose:
A and B are your treatment condition, C is your control. You're not just
building three pages — you're testing a hypothesis, which is exactly what
the next slide walks through.

### Slide 18 — Lab: what to actually compare

Once all three sessions are done, put screenshots of A, B, and C side by
side — actually side by side, on one screen, not toggling between browser
tabs from memory.

First question: where do A and B *match*? Same accent color, same spacing
rhythm, same corner radius on cards and buttons? If your tokens-plus-doc-
plus-rule setup is doing its job, A and B — built in two sessions with
zero shared memory of each other — should look like they came from the
same designer, because in the sense that actually matters, they did: they
both read the same tokens file.

Second question: where does C *drift*? A different blue than A and B
picked? A different button shape — maybe fully rounded where A and B used
`--radius-base`'s more modest curve? Inconsistent spacing that doesn't
follow any visible scale? This is the drift from Slide 5 made visible and
concrete, sitting right next to two pages that don't have it.

And here's the sentence I want you to really sit with, because it's the
part of this lab most people get wrong on their first pass: if A and B
*also* disagree somewhere — say they both used the tokens correctly but
picked different corner-radius values for a component type your doc never
actually mentioned — that is not the lab failing. That's not "well, tokens
don't really work then." That's a **gap in the tokens or the doc** that
you now know needs closing, discovered exactly the way Slide 16's loop
says it should be discovered: by rendering and comparing, then feeding
what you found back into the artifact. A mismatch between A and B is data
about your design system doc's completeness, not a verdict on the whole
method.

---

## Section 8 — Wrap-Up (Slides 19–22) — ~10 min

### Slide 19 — Deliverable

What you're handing in has four parts. The tokens file and the design
system doc themselves — the actual artifacts, not a description of them.
The `CLAUDE.md`/`AGENTS.md` snippet you added. Screenshots from Sessions
A, B, and C, side by side the way you just compared them. And a short
writeup: where A and B matched, where C drifted, and — this last part is
the one that shows you actually understood today's material rather than
just following steps — whether any mismatch you found *between* A and B
traces back to something the tokens or doc left underspecified. That last
question is where the real thinking happens; don't skip it just because
the screenshots themselves are the more visually satisfying part of the
deliverable.

### Slide 20 — Discussion questions

Three questions worth sitting with, and I don't have a single clean
answer to any of them — they're genuinely open, and your answer will
probably depend on the kind of product you're building.

When does a design system doc get so detailed that it costs more to
maintain than the drift it prevents? There's clearly a point of
diminishing returns — a doc trying to specify every possible component
state for every possible screen becomes its own maintenance burden, and a
stale, over-detailed doc can mislead an agent worse than a short,
accurate one. Where's that line for your team?

Should tokens live with functional specs, or stay separate with their own
update cadence? Design tokens tend to change on a different rhythm than
feature specs — a rebrand happens far less often than new features ship —
which might argue for keeping them apart. But keeping them apart also
means one more place an agent has to know to look. Which cost matters
more in your context?

And: how does this whole approach change for designs that are
*deliberately* meant to vary — generative art, a page that's supposed to
look different every time you load it? Everything today assumed
consistency was the goal. What does "design tokens" even mean for a
project whose entire point is that it *shouldn't* be reproducible?

### Slide 21 — Recap

Let's pull it back together. The starting diagnosis: vague adjectives are
where session-to-session drift comes from. Not a prompting problem — a
specification problem, in exactly Module 6's sense of that word.

The fix has five layers, and I want you to be able to name what gap each
one closes, not just recite the list: tokens give you values instead of
prose, so there's nothing left to interpret differently between sessions.
The design doc gives you rationale — the why and the how-they-combine that
tokens alone can't carry. The repo rule gives you enforcement — it's the
hook that makes sure the first two artifacts actually get read. The Skill,
where it's warranted, gives you construction — enforcement that doesn't
depend on the agent remembering anything at all. And visual review gives
you verification — catching the category of bug that a clean-looking
text diff structurally cannot see.

Five layers, five different gaps. Drop any one of them and Slide 12's
failure table tells you exactly which gap reopens.

And zoom all the way out: this is the same discipline as Module 6's DDD,
just aimed at pixels instead of behavior. Move the decision into a file.
Make the file get read. Verify the output actually matches. That pattern
is going to keep coming back for the rest of this course, in new
contexts, because it's not really a UI technique or a coding technique —
it's the general answer to "how do I get consistent output from a system
that has no memory between runs."

### Slide 22 — Next module

Next time: Module 8, Plan-First Workflows. We're going to separate
*planning* from *execution* — approval gates, ADRs, and why an ephemeral
plan is solving a genuinely different problem than a durable spec or a
tokens file. Notice the shape of that distinction already: today's
artifacts — tokens, the design doc — are meant to be durable, read again
and again, session after session. A plan, it turns out, wants to behave
differently, and next module is about why treating a plan like a durable
spec is its own kind of mistake. Bring your tokens-and-doc setup from
today; we'll be building directly on the idea that some artifacts persist
and some shouldn't.

Go run your three sessions. See you with your screenshots.
