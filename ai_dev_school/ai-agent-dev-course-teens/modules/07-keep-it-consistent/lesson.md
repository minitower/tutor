# Module 7 — Keep It Looking Consistent

## Big idea

If you don't write your colors, fonts, and spacing down somewhere real,
the agent has to guess every session — and it'll guess differently each
time. The fix: make a "style sheet" file with the actual values (real
color codes, real font names, real spacing numbers), and tell the agent
to always use it instead of picking its own.

```css
:root {
  --color-background: #14161a;
  --color-accent: #ffb703;
  --font-heading: "Poppins", sans-serif;
  --space-unit: 8px;
}
```

Specific values are what make it consistent. "Make it look cool and
modern" is exactly the kind of instruction that looks different every
single time you ask.

## Why it matters

A project built page by page without this ends up looking like it was
stitched together from five different projects. This is one file that
prevents that, permanently, for the rest of the course.

## Hands-on task

1. Make a real style-sheet file for your project with actual color
   codes, a font, and spacing values.
2. Add a short note in your project's instructions file telling the
   agent: "always check this file before styling anything, and don't
   introduce new colors/fonts/spacing outside it."
3. In one session, build one page/screen using only this file as the
   style guide.
4. In a **completely separate, fresh session**, build a second, different
   page/screen — same rule.
5. Put both side by side.

## Checkpoint

- Do the two pages actually look like they belong to the same project?
- Try it once *without* pointing the agent at the style file — just "make
  it look nice." How different does that one look?

## Supervisor note

Standard supervision. This is a satisfying module to watch — the
side-by-side comparison makes the point visually, no explanation needed.
