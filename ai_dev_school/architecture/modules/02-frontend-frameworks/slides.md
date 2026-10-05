---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 2
## Frontend Frameworks: How to Choose
### React, Vue, Angular, Svelte, Next, Nuxt, Astro — and SPA vs SSR vs SSG

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- Why a framework at all: from jQuery to components
- Reactivity models
- Rendering strategies: SPA, SSR, SSG, ISR, islands
- UI libraries and meta-frameworks
- Tooling and styling
- Beyond the browser
- Decision matrix and performance
- Lab: two parts of "Slot"

---

<!-- Slide 3 -->
## Learning objectives

- Understand what a framework does and why life without one hurts
- Tell SPA, SSR and SSG apart and know what each means for SEO and speed
- Know the strengths of React, Vue, Angular, Svelte and their meta-frameworks
- Choose a framework with arguments, not hype

---

<!-- Slide 4 -->
## The problem: keeping data and screen in sync

```js
// jQuery style: every data change is a manual DOM edit
slots = slots.filter(s => s.id !== bookedId);
$('#slot-' + bookedId).remove();
$('#free-count').text(slots.length);
if (slots.length === 0) $('#empty').show();
// forget one line — the screen lies
```

A framework solves this: **you describe how the screen depends on the data, and it updates the DOM for you**.

---

<!-- Slide 5 -->
## Components, props, state

```jsx
function SlotList({ slots, onBook }) {          // props — input
  const [selected, setSelected] = useState(null); // state
  if (slots.length === 0) return <p>No free slots</p>;
  return (
    <ul>
      {slots.map(s => (
        <SlotItem key={s.id} slot={s}
          active={s.id === selected}
          onClick={() => setSelected(s.id)} />
      ))}
    </ul>
  );
}
```

UI = function(state). A component is a reusable piece of interface.

---

<!-- Slide 6 -->
## Reactivity models

| Model | How it learns about changes | Who uses it |
|---|---|---|
| **Virtual DOM** | Re-renders a tree in memory and diffs it | React |
| **Proxies / signals** | Tracks who read a value, updates only them | Vue, Solid, Angular (signals), Preact signals |
| **Compiler** | Turns a component into targeted DOM updates at build time | Svelte |

Users usually can't see the difference; bundle size and speed on cheap phones can.

---

<!-- Slide 7 -->
## Rendering strategies

| Strategy | Where HTML is built | When |
|---|---|---|
| **SPA** | In the browser, after JS loads | Admin panels, dashboards, anything behind login |
| **SSR** | On the server, per request | Pages that need SEO and fresh data |
| **SSG** | At build time, once | Landing pages, blogs, docs |
| **ISR** | At build time + rebuild on a timer | Catalogs that change rarely |
| **Islands** | Static HTML + interactive "islands" | Content sites with a bit of interactivity |

---

<!-- Slide 8 -->
## SPA vs SSR: what a search engine sees

**SPA:** the server sends an empty page and a big JS file

```html
<body><div id="root"></div><script src="app.js"></script></body>
```

**SSR / SSG:** the server sends ready HTML, JS "brings it to life" (**hydration**)

```html
<body><h1>Beard Barbershop</h1><ul><li>Fri 15:00 — free</li>...</ul></body>
```

Search engines can run JS, but slower and not always. For public pages — SSR/SSG.

---

<!-- Slide 9 -->
## React Server Components

- Some components run **only on the server**: they query the DB and never ship in the bundle
- Client components (`"use client"`) only where interactivity is needed
- Less JS in the browser, data without a separate API layer
- The cost: a harder mental model, you need a meta-framework (Next.js)

---

<!-- Slide 10 -->
## UI libraries

| | Strengths | Weaknesses |
|---|---|---|
| **React** | Largest ecosystem and job market | Lots of "choose it yourself" decisions |
| **Vue** | Gentle learning curve, batteries included | Fewer jobs in some markets |
| **Angular** | Full framework, strict structure, TypeScript | Heavy, steep learning curve |
| **Svelte** | Least code and JS, a compiler | Smaller ecosystem |
| **Solid** | Signals, very fast | Small community |

---

<!-- Slide 11 -->
## Meta-frameworks

A UI library renders components. A **meta-framework** adds routing, data loading, SSR/SSG, server code, builds.

| Library | Meta-framework |
|---|---|
| React | **Next.js**, React Router (ex-Remix) |
| Vue | **Nuxt** |
| Svelte | **SvelteKit** |
| Any | **Astro** — content + islands from any components |

---

<!-- Slide 12 -->
## Tooling

- **Node.js** — runs build tools and server code
- **npm / pnpm** — packages; `package.json` + a lock file
- **Vite** — a dev server with instant reload and a production build
- **TypeScript** — types catch errors before running; a hint for agents too
- **ESLint, Prettier** — one consistent style

```bash
npm create vite@latest slot-admin -- --template react-ts
```

---

<!-- Slide 13 -->
## Styling

| Approach | How | When |
|---|---|---|
| CSS modules | Plain CSS, class names are scoped | Simple and reliable |
| **Tailwind** | Utility classes right in the markup | Fast, consistent; popular with agents |
| Component libraries | shadcn/ui, MUI, Vuetify, Ant Design | Admin panels: tables, forms, modals ready-made |

For agents one thing matters: **shared design tokens** (colors, spacing), or every screen ends up in its own style.

---

<!-- Slide 14 -->
## Beyond the browser

| Task | Options |
|---|---|
| Mobile app | React Native, Flutter, native Swift/Kotlin |
| Desktop | Tauri (light, Rust), Electron (heavy, but familiar) |
| "Almost an app" without app stores | **PWA** — a site with offline mode and a home-screen icon |

For "Slot" a PWA is enough: the barber installs the admin panel on their phone like an app.

---

<!-- Slide 15 -->
## Decision matrix

| Task | Recommendation |
|---|---|
| Content site, blog, landing page | **Astro** or SSG |
| SEO + an app in one | **Next.js** / **Nuxt** |
| Internal admin, dashboard | **SPA**: React or Vue + Vite |
| Large enterprise team | **Angular** |
| The lightest possible interactivity | **Svelte / SvelteKit** |

Plus: what the team knows, which hosting, whom you can hire.

---

<!-- Slide 16 -->
## Questions before choosing

1. Do you need **SEO**? → SSR/SSG
2. How much **interactivity**? → from islands to SPA
3. What does the **team already know**?
4. Are there **ready-made components** for the job?
5. Where will it be **hosted**? (Vercel and Next.js, static on a CDN)
6. Whom can you **hire** a year from now?

Record the answer in an ADR.

---

<!-- Slide 17 -->
## Frontend performance

- **Core Web Vitals:** LCP (main content load), INP (response to input), CLS (layout shifts)
- The main enemy is **JS size**: every kilobyte must be downloaded, parsed and executed
- Techniques: code splitting, lazy loading, image optimization, fewer dependencies
- **Lighthouse** in DevTools — a free audit in a minute

---

<!-- Slide 18 -->
## "Slot": two different jobs — two approaches

| | Public page | Admin panel |
|---|---|---|
| Who looks at it | Clients and search engines | Only the barber |
| SEO | Critical | Not needed |
| Interactivity | A little: pick a slot | A lot: calendar, tables |
| Approach | SSR/SSG (Next.js or Astro) | SPA (React + Vite) |

One product doesn't have to mean one framework.

---

<!-- Slide 19 -->
## Lab

1. Start a mock API from the Module 1 OpenAPI (e.g. Prism)
2. "Slot" public page: SSR/SSG, services and free slots, a booking form
3. Admin panel: SPA, list of bookings, cancel a booking
4. Run **Lighthouse** on both
5. **With an agent:** give the agent the user stories and design tokens, ask it to build the admin screens; check the result against the acceptance criteria

---

<!-- Slide 20 -->
## Deliverable

- Two frontends working against the mock API
- Lighthouse reports for both
- A one-page ADR: "why this framework"
- A list of places where the agent drifted from the acceptance criteria

---

<!-- Slide 21 -->
## Recap and next module

- A framework keeps data and screen in sync for you
- SPA for apps behind login, SSR/SSG for pages that need SEO
- Choice = SEO + interactivity + team + ecosystem + hiring
- Next: **Module 3 — Backend Languages & Frameworks** — a real API instead of the mock
