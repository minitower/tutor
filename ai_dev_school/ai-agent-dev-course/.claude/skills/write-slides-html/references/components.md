# Component snippets

Copy-paste starting points for every reusable pattern in `deck.css`.
Adjust text/counts; don't change the class names or you lose the styling.

## `.compare` — before/after, bad/good

Two cards, red border on the left, green on the right. Use only for a
real problem→fix pair.

```html
<div class="compare">
  <div class="card before">
    <h4>До</h4>
    <p>«Расплывчатый или плохой пример»</p>
  </div>
  <div class="card after">
    <h4>После</h4>
    <p>«Конкретный, проверяемый пример»</p>
  </div>
</div>
```

Also valid with a `<pre><code>` instead of `<p>` inside either card
(see module 05 slide 7 for a worked example with code on both sides).

## `.trio` — 3 neutral cards

No good/bad connotation — for taxonomies, options, parallel categories.

```html
<div class="trio">
  <div class="card"><h4>Label A</h4><p>One or two sentences.</p></div>
  <div class="card"><h4>Label B</h4><p>One or two sentences.</p></div>
  <div class="card"><h4>Label C</h4><p>One or two sentences.</p></div>
</div>
```

For 2 cards instead of 3, keep the `.trio` class (for `.card` styling)
and override the grid inline so you don't get an empty third column:

```html
<div class="trio" style="grid-template-columns: 1fr 1fr;">
  <div class="card">...</div>
  <div class="card">...</div>
</div>
```

## Problem + mitigation (inline pattern, not yet a class)

Nest a small green-bordered block inside a `.card.before` to separate
"here's the antipattern" from "here's the fix," instead of jamming both
into one `<p>` with a `<br>`.

```html
<div class="card before">
  <h4>Название антипаттерна</h4>
  <p>Что идёт не так.</p>
  <div style="margin-top:.7rem; padding:.5rem .8rem; border:1px solid rgba(55,230,176,.4); border-radius:8px; background:rgba(55,230,176,.06);">
    <strong style="color:var(--accent-2); font-size:.85rem;">Смягчение</strong>
    <p style="margin:.2rem 0 0;">Конкретное действие, которое это исправляет.</p>
  </div>
</div>
```

If a fourth slide ends up needing this, promote it into `deck.css`
proper as something like:

```css
.mitigation { margin-top:.7rem; padding:.5rem .8rem; border:1px solid rgba(55,230,176,.4); border-radius:8px; background:rgba(55,230,176,.06); }
.mitigation .label { color:var(--accent-2); font-size:.85rem; font-weight:700; }
```

and swap the inline styles above for `<div class="mitigation"><span class="label">Смягчение</span><p>...</p></div>`.

## `.svg-scene` — centered SVG wrapper

```html
<div class="svg-scene">
  <svg viewBox="0 0 560 200" xmlns="http://www.w3.org/2000/svg">
    ...
  </svg>
</div>
```

Add `small` for a compact square diagram (caps width at 420px):

```html
<div class="svg-scene small">
  <svg viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg">
    ...
  </svg>
</div>
```

To shrink further on a crowded slide, cap the rendered size directly on
the `<svg>` (viewBox stays the same, just the display size changes):

```html
<div class="svg-scene small" style="margin:.4rem 0 0;">
  <svg viewBox="0 0 240 240" style="max-width:210px;" xmlns="http://www.w3.org/2000/svg">
```

## `.icon-compare` — two icons with "vs"

```html
<div class="icon-compare">
  <div class="side">
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">...</svg>
    <span class="ic-label">Label A</span>
    <span class="ic-desc">One line describing it</span>
  </div>
  <div class="vs">vs</div>
  <div class="side">
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">...</svg>
    <span class="ic-label">Label B</span>
    <span class="ic-desc">One line describing it</span>
  </div>
</div>
```

## `.flow-loop` — horizontal step pipeline

```html
<div class="flow-loop">
  <div class="flow-step" style="--c:var(--accent)"><span class="flow-label">Шаг 1</span><span class="flow-desc">что происходит</span></div>
  <div class="flow-arrow">→</div>
  <div class="flow-step" style="--c:var(--accent-3)"><span class="flow-label">Шаг 2</span></div>
  <div class="flow-arrow">→</div>
  <div class="flow-step" style="--c:var(--accent-2)"><span class="flow-label">Шаг 3</span></div>
</div>
<p class="flow-repeat">↻ optional repeat/summary line under the row</p>
```

`--c` sets the step's border/label color per-step; cycle through
`var(--accent)`, `var(--accent-3)`, `var(--accent-2)` for 3+ steps.
`flow-desc` is optional — omit it for a plain label-only step.

## `.flow-vertical` — vertical pipeline with a decision node

```html
<div class="flow-vertical">
  <div class="fv-step">Шаг 1</div>
  <div class="fv-arrow">↓</div>
  <div class="fv-step fv-decision">Развилка?</div>
  <div class="fv-arrow">↓</div>
  <div class="fv-step">Шаг 2</div>
</div>
```

## `.trace-log` — annotated step list

```html
<ol class="trace-log">
  <li><span class="tag plan">План</span> текст шага</li>
  <li><span class="tag action">Действие</span> <code>tool_call(...)</code></li>
  <li><span class="tag obs">Наблюдение</span> что вернулось</li>
  <li><span class="tag danger">Опасно</span> формулировка риска</li>
</ol>
```

`tag` classes: `plan` (blue), `action` (pink), `obs` (green), `danger`
(red). Works as a plain `<ul>`/`<ol>` too — the `.tag` styling doesn't
depend on the list type.

## Code / spec blocks

```html
<pre><code>## Раздел
Содержимое строкой.
## Другой раздел
Ещё содержимое.</code></pre>
```

Gets a dark background, rounded corners, and three colored dots
top-left automatically (`.slide pre::before`) — don't add your own
window-chrome markup. HTML-escape `<`/`>` inside (`&lt;`, `&gt;`) if the
example itself contains angle brackets.

For inline-colored spans inside a code block (e.g. a file tree), use
inline `style="color:var(--accent)"` on a `<span>` — see
`icons.md`'s file-tree example.
