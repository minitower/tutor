---
name: write-slides-html
description: >
  How to write, extend, or restyle a course module's slides.html deck in
  ai_dev_school/ai-agent-dev-course — the hand-authored dark-theme HTML
  slide format (not the plain Marp slides.md/slides.ru.md). Covers the
  page skeleton, the reusable component vocabulary (compare cards, trio
  grids, flow loops, SVG icon scenes) defined in assets/deck.css, and the
  mandatory local-server verification workflow. Use this skill whenever
  asked to add slides, add an SVG/diagram/visual to a slide, restyle or
  rebalance a slide's content, or build a new module's slides.html from
  scratch — even if the user just says "add a picture" or "make this
  slide match the others." Do NOT use it for edits to slides.md or
  slides.ru.md (the Marp sources never carry visuals — see below).
---

# Writing slides.html for this course

Every module folder has three slide artifacts: `slides.md` (English Marp
source), `slides.ru.md` (Russian Marp source), and `slides.html` (a
hand-authored interactive deck, always in Russian, styled by
`../../assets/deck.css` and driven by `../../assets/deck.js`). This skill
is about `slides.html` only.

**`slides.html` never gets mirrored into the `.md` files, and the `.md`
files never carry visuals.** Confirmed by modules 01–03: the SVGs,
comparison cards, and taxonomy grids added to `slides.html` have no
counterpart in `slides.ru.md`. Don't "keep them in sync" — that's not
how this repo works. If a user wants the actual *text content* of a
slide changed (not just its visual treatment), ask whether that should
land in the `.md` sources too; don't assume.

`slides.html` sections correspond 1:1, in order, to the slides in
`slides.ru.md` by topic — but `slides.html` is allowed to say *more*:
extra examples, diagrams, taxonomy slides that don't exist in the Marp
version. That asymmetry is the established house style, not a bug to fix.

## Before touching anything

1. Read the target `slides.html` in full. Don't guess slide numbers from
   memory or from the `.md` file — count them:
   ```bash
   grep -n '<section\|<h2>' modules/NN-.../slides.html
   ```
   Slide N is the Nth `<section class="slide"...>` in document order.
   There are no IDs and no numbering attributes — `deck.js` just walks
   `document.querySelectorAll(".slide")`, so inserting, deleting, or
   reordering `<section>` blocks is always safe as long as tags balance.
2. After editing, re-run the same `grep -c '<section'` /
   `grep -c '</section'` check and diff the `<h2>` list against your
   intent. This is the cheap way to catch a slide you accidentally
   duplicated or dropped while restructuring.

## Page skeleton

```html
<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Модуль N — <Name></title>
<link rel="stylesheet" href="../../assets/deck.css">
</head>
<body>
<div class="progress" id="deck-progress"></div>
<main class="deck">

<section class="slide" data-layout="title">
  <p class="kicker">Модуль N</p>
  <h1>Module Name</h1>
  <h2>Subtitle</h2>
  <p class="course">Agentic Software Development: From Specs to Shipped Code</p>
</section>

<section class="slide">
  <h2>...</h2>
  ...
</section>

<!-- ... more <section class="slide"> ... -->

<section class="slide" data-layout="divider">
  <p class="num">→ NN+1</p>
  <h2>Далее: <Next module></h2>
  <p>Recap of this module.</p>
  <p><em>Teaser for the next one.</em></p>
</section>

</main>
<div class="hud">
  <button class="nav-btn" data-nav="prev" aria-label="Назад">‹</button>
  <span id="deck-counter" class="counter"></span>
  <button class="nav-btn" data-nav="next" aria-label="Вперёд">›</button>
  <button class="nav-btn" data-nav="fullscreen" aria-label="Полный экран">⛶</button>
</div>
<script src="../../assets/deck.js"></script>
</body>
</html>
```

Every deck is exactly this shape: a title slide, N content slides, a
divider slide pointing at the next module. `deck.js` needs nothing else
— no config, no per-slide markup beyond `class="slide"`.

## Layout types

| `data-layout` | When | Notes |
|---|---|---|
| *(none)* | almost every slide | `<h2>` + body, left-aligned |
| `title` | slide 1 only | big gradient `<h1>`, centered |
| `divider` | section breaks, "next module" | huge faint number + centered text |
| `quote` | one punchy idea, no bullets | giant centered italic `<blockquote>` |

Don't force content into `quote` just because a slide *feels* important —
it only works for a single short line. If you need bullets or a card
grid alongside the quote, append them below the `<p class="cite">` (see
module 02 slide 5 for a working example) rather than switching layouts.

## The component vocabulary

Everything reusable lives in `assets/deck.css`, shared by all modules.
**Reuse a class before inventing a new one** — check
`references/components.md` for the full list with copy-paste snippets.
Quick index of what exists and what it's *for* (not just what it looks
like):

- **`.compare` + `.card.before/.after`** — a genuine bad-vs-good or
  before-vs-after pair. Red border = before/bad, green = after/good.
  Don't use this for two things that are just *different categories*
  (e.g. "context vs. instructions") — that's not a good/bad pair, and
  coloring one of them red is misleading. Use `.trio` instead.
- **`.trio`** — 3 neutral cards, no good/bad connotation. For a 2-card
  version, keep the class (for the card styling) but override the grid
  inline: `<div class="trio" style="grid-template-columns: 1fr 1fr;">`.
- **`.svg-scene` / `.svg-scene.small`** — centering wrapper for any
  inline `<svg>` diagram. Use `.small` (max-width 420px) for a compact
  square diagram (loops, small icon groups); omit it for a wide scene
  (a multi-element flow across the slide).
- **`.icon-compare`** — two icons side by side with a "vs" divider
  between them, each with a label and one-line description.
- **`.flow-loop` / `.flow-step`** — a horizontal row of labeled pipeline
  steps with arrows between them.
- **`.flow-vertical` / `.fv-step` / `.fv-decision`** — same idea,
  vertical, for a decision/approval pipeline.
- **`.trace-log` + `.tag.plan/.action/.obs/.danger`** — a list of
  annotated steps (used for agent traces and "here's what's risky"
  lists).
- **`<pre><code>`** — code or spec-text blocks. Comes with a built-in
  three-dot "terminal" decoration via `::before` that needs its default
  top padding — see the overflow-fix section below before you touch it.
- **`<table>`** — plain comparison tables, already themed.

There is no pre-built "problem + mitigation" component. The pattern used
in module 03 (a small green-bordered sub-block nested inside a `.card
.before`) is inline-styled, not a class, because it's only used twice so
far. If a fourth slide needs it, promote it to a real `.mitigation` class
in `deck.css` instead of copy-pasting the inline style a fourth time —
see `references/components.md` for the exact style block to lift out.

## Reusable SVG icons

Module 01 established a small icon vocabulary (user, agent/robot,
document, checkmark, danger/terminal, file tree, N-node loop) that
modules 02–03 have been reusing rather than redrawing. Pull the actual
markup from `references/icons.md` — don't redraw an agent robot from
scratch, copy the existing path data and restyle the color if needed.

All icon strokes/fills use CSS variables (`var(--accent)`,
`var(--accent-2)`, etc.), never hardcoded hex, so they stay correct in
whatever theme the page renders in.

## Color semantics (already encoded in `:root` in deck.css)

| Variable | Color | Established meaning |
|---|---|---|
| `--accent` | blue | neutral/primary — user, spec/document, data |
| `--accent-2` | green | positive — success, mitigation, "after"/good |
| `--accent-3` | pink | agent / action taken |
| `--danger` | red | risk, antipattern, "before"/bad |
| `--fg-dim` | grey | secondary/de-emphasized text |

Keep new diagrams consistent with this: an agent icon is pink, a
checkmark is green, a risky terminal command is red. Don't pick colors
by what looks nice in isolation — pick them by what the color already
means elsewhere in the deck.

## Making an edit: the actual steps

1. Find the target slide(s) by grepping `<h2>` (see above).
2. Pick the smallest component that fits — a one-line addition doesn't
   need a new `<div>` wrapper; a genuine new idea might need its own
   slide rather than cramming into an existing one.
3. Write the HTML directly into `slides.html`. No build step, no
   templating — the file you edit is the file that gets served.
4. **Verify it renders** (mandatory — see next section). A change that
   looks reasonable as markup can silently overflow the slide at real
   presentation size.
5. Re-check the slide count/heading list from step 1 of "Before touching
   anything" if you inserted, removed, or reordered slides.

### Slide density budget

A slide is roughly full at: `<h2>` + up to ~4 bullets + **one** visual
(a code block, *or* an SVG scene, *or* a card grid — not two). If a slide
already has a paragraph, a list, and a blockquote, adding an SVG on top
will very likely overflow at 16:9 — either trim the existing text or
shrink the visual (see overflow fixes below), and verify.

## Verification workflow (do this before calling any visual change done)

Opening `slides.html` directly as a `file://` URL does **not** work for
checking your work — it loads as a static, unstyled snapshot with no CSS
or JS (relative asset paths don't resolve, so the whole dark theme and
the slide-by-slide carousel behavior are silently missing). You have to
serve it.

1. A launch config already exists at the repo root
   (`C:\Users\raven\Projects\tutor\.claude\launch.json`, name
   `course-slides`) that serves `ai_dev_school/ai-agent-dev-course/` on
   `localhost:8123`. Start it with `preview_start` using that name — do
   not use Bash to run your own server, and don't recreate the config if
   it's already there.
2. Navigate to `http://localhost:8123/modules/NN-.../slides.html?v=1#S`
   where `S` is the slide number you want to check.
   - **The `?v=N` query bump matters.** `deck.js` reads `location.hash`
     only once, at initial script load — there's no `hashchange`
     listener. Navigating to a new `#hash` on a URL that only differs by
     hash (same origin, same path, same query) is treated as an
     in-page navigation and does *not* reload the script, so the slide
     won't change. Increment `?v=` on every navigation where you need a
     real reload (checking a new slide, or re-checking after an edit).
   - Otherwise, land on slide 1 and use `ArrowRight`/`ArrowLeft` key
     presses (one at a time — `repeat > 1` can trigger a "page navigated
     during key sequence" abort in this environment) to step to the
     slide you want.
3. **Resize to real presentation size before judging overflow**:
   `resize_window` to `1440x810` (the deck is authored for 16:9). The
   pane's default small viewport (~800x450 or less) will make normal,
   correctly-fitting slides look cramped or scrolled — that's a false
   positive, not a real bug. Judge fit at 1440x810, not at the default
   size.
4. Wait about a second after navigating/pressing a key before taking a
   screenshot. The CSS transition between slides is 0.35s; a screenshot
   taken immediately can catch a ghosted mid-fade overlap between the
   old and new slide, which looks like a rendering bug but isn't.
5. If you're unsure whether a slide is actually overflowing (vs. just a
   stray inner scrollbar on a `<pre>`), check programmatically instead of
   eyeballing it:
   ```js
   const s = document.querySelector('.slide.active');
   ({fits: s.scrollHeight <= s.clientHeight, scrollHeight: s.scrollHeight, clientHeight: s.clientHeight})
   ```
   via `javascript_tool`. `scrollHeight > clientHeight` on `.slide`
   itself means the slide really overflows; a scrollbar confined to one
   `<pre>` is usually harmless and often present even at exact-fit sizes.
6. When done, reset the viewport (`resize_window preset:"desktop"`) and
   stop the preview server (`preview_stop`) — don't leave it running
   across turns.

## Fixing overflow

In order of preference:

1. **Shrink a `<pre><code>` block** via inline style on the `<code>` tag:
   `style="font-size:.85rem; line-height:1.35;"`. Never shrink the
   `<pre>`'s own `padding-top` — that space is reserved for the
   three-dot decoration (`.slide pre::before`, absolutely positioned);
   shrinking it makes the first code line overlap the dots.
2. **Tighten a code block's content** — drop blank lines between
   sections in a template/spec example. A `## Section` block doesn't
   need a blank line before every header to stay readable.
3. **Shrink an SVG scene** via inline `style="max-width:NNNpx;"` directly
   on the `<svg>` tag (overrides `.svg-scene.small`'s default 420px).
   The `viewBox` stays the same — you're just capping the rendered size,
   not redrawing it.
4. **Cut content**, if none of the above gets you there. A slide that
   needs a fifth trick to fit probably wants to be two slides.

## Gotchas

- **Inline `<style>` blocks inside an `<svg>` are not scoped to that
  SVG** — they apply to the whole document, same as any other `<style>`
  tag. This is harmless as long as class names used inside one SVG's
  `<style>` (e.g. `.node`, `.lbl`, `.dot`) aren't reused by a *different*
  SVG's `<style>` block **in the same file** with different intended
  styling. Reusing the same names across *different modules'*
  `slides.html` files is fine — those are separate documents.
- **This deck is intentionally zero-build**: raw HTML, one shared CSS
  file, one shared JS file, no bundler, no framework, no new
  dependencies. Don't introduce one to solve a slide-content problem.
- **Don't touch `deck.js`** for a one-slide need. It's shared by every
  module; a behavior change there affects the whole course.
