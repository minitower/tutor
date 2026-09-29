---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->

# Keep It Looking Consistent

Module 4 — Build With AI

---

<!-- Slide 2 -->

## Today

- Why the same agent, asked twice, styles things differently
- The fix: a real "style sheet" file with real values
- Hands-on: build two pages, two fresh sessions, one style file
- Checkpoint: do they actually match?

---

<!-- Slide 3 -->

## Recap: Module 3

- Big idea: write down what you want *before* the agent builds it
- A short plan beat winging it, especially once the feature got bigger
- Today: the same move, aimed at something narrower — what your project
  actually *looks* like

---

<!-- Slide 4 -->

## The Problem

- A fresh agent session has no memory of last session's choices
- Ask for a "clean, modern" login page twice, in two separate sessions
- Both results might look great. They will not look like the same app

---

<!-- Slide 5 -->

## The Big Idea

**If you don't write your colors, fonts, and spacing down somewhere
real, the agent guesses — differently, every time.**

Fix: one file, real values, and a rule to always check it before
styling anything.

---

<!-- Slide 6 -->

## What a Style Sheet Actually Looks Like

```css
:root {
  --color-background: #14161a;
  --color-accent: #ffb703;
  --font-heading: "Poppins", sans-serif;
  --space-unit: 8px;
}
```

Real hex codes. A real font name. A real number. Nothing to interpret.

---

<!-- Slide 7 -->

## Specific Beats Vague — Every Time

- "Make it look cool and modern" → different result every session
- `--color-accent: #ffb703;` → the exact same color every session
- This is Module 2's lesson again: vague asks get guesses, specific
  asks get what you meant

---

<!-- Slide 8 -->

## Make the Agent Actually Use It

Add one line to your project's instructions file:

> "Always check `style.css` before styling anything. Don't introduce
> new colors, fonts, or spacing outside of it — add to the file
> instead."

A file the agent doesn't know to check is just a file.

---

<!-- Slide 9 -->

## Without the File vs. With It

**Without:** "make it look nice," twice, two sessions → two different
color schemes, two different fonts, spacing that doesn't match.

**With:** same style file, two sessions → same colors, same font, same
rhythm — even though neither session saw the other one build.

---

<!-- Slide 10 -->

## Why It Matters

- Build page by page with no shared style file and it ends up looking
  stitched together from five different projects
- One file, written once, fixes this for the rest of the course
- This isn't extra work — it's less work than fixing mismatched pages
  later

---

<!-- Slide 11 -->

## Your Turn: Hands-On

1. Write a real style-sheet file — actual colors, a font, spacing values
2. Add the "always check this file" rule to your instructions file
3. **Session A:** build one page/screen using only the style file
4. **Session B — completely fresh session:** build a different
   page/screen, same rule
5. Put both pages side by side

---

<!-- Slide 12 -->

## What to Actually Compare

- Same accent color in both?
- Same font, same heading style?
- Same spacing rhythm — or does one feel cramped and the other loose?
- Anywhere they *don't* match is a gap in your style file, not bad luck

---

<!-- Slide 13 -->

## Checkpoint

- Do the two pages actually look like they belong to the same project?
- Now try it once *without* pointing the agent at the style file — just
  "make it look nice." How different does that version look?

---

<!-- Slide 14 -->

## Recap

- A fresh session has no memory — vague style instructions drift every
  time
- Real values in a real file remove the guessing
- A rule in your instructions file is what makes the agent actually
  open it
- Two sessions, one file, matching pages — that's the whole trick

---

<!-- Slide 15 -->

## Next Up

**Module 5 — Plan Before You Build**

For a bigger change, you'll agree on *how* it's going to be built before
any code changes — same instinct as today, aimed at the approach instead
of the visuals.
