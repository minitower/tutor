# Module 2 — Frontend Frameworks: How to Choose

## Learning objectives
- Understand how a modern frontend works under the hood
- Know the main frameworks and meta-frameworks and what each is good at
- Pick a framework for a task with arguments, not hype

## Lecture outline
1. From jQuery to components: DOM, components, props, state
2. Reactivity models: virtual DOM (React), proxies/signals (Vue, Solid, Angular signals), compiler (Svelte)
3. Rendering strategies: SPA, SSR, SSG, ISR, islands, hydration, React Server Components; what each means for SEO and speed
4. UI libraries: React, Vue, Angular, Svelte, Solid; ecosystem, learning curve, job market
5. Meta-frameworks: Next.js, Nuxt, SvelteKit, Astro, React Router (ex-Remix); routing, data loading, server code
6. Tooling: Node.js, npm/pnpm, Vite, TypeScript, linters
7. Styling: CSS modules, Tailwind, component libraries (shadcn/ui, MUI, Vuetify)
8. Beyond the browser: React Native, Flutter, Tauri/Electron, PWA
9. Decision matrix: SEO need, interactivity, team skills, ecosystem, hiring, hosting
   - Content site / blog / landing → Astro or SSG
   - SEO + app in one → Next.js / Nuxt
   - Internal admin / dashboard → SPA (React or Vue + Vite)
   - Large enterprise team → Angular
10. Frontend performance: bundle size, Core Web Vitals, Lighthouse

## Lab
Build the "Slot" public page (SSR/SSG, needs SEO) and the admin panel (SPA) against a mock API. Run Lighthouse on both.
- **With an agent:** give the agent the user stories from Module 1 and the design tokens; ask it to build the admin screens; review the output against the acceptance criteria.

## Deliverable
Two frontends + Lighthouse reports + a one-page ADR "why this framework".
