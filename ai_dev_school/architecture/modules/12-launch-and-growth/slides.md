---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- Slide 1 -->
# Module 12
## Launch & Growth: Getting Your First Users
### How search engines and social feeds work, and how to plan a launch

*Modern Application Architecture: From Idea to a Live Product*

---

<!-- Slide 2 -->
## Session plan

- How a search engine works
- Technical SEO
- Google and Yandex
- Content SEO
- How social media feeds rank
- Launch channels
- Positioning and the landing page
- Funnel and metrics
- Analytics, privacy, consent
- Lab

---

<!-- Slide 3 -->
## Learning objectives

- Understand how search engines and social feeds decide what a person sees
- Make an app technically ready to be indexed and measured
- Choose channels that fit your audience
- Plan a launch with clear metrics

---

<!-- Slide 4 -->
## "Build it and they will come" doesn't work

- Thousands of apps launch every day
- Users find a product three ways: **search**, **recommendations** (feeds, friends), **direct** (ads, links)
- Each path has its own algorithm, and it can be understood
- Promotion is an engineering problem too: hypothesis → experiment → metric

---

<!-- Slide 5 -->
## How a search engine works

1. **Crawling** — a bot follows links and downloads pages
2. **Rendering** — runs JS to see the final content (expensive, often deferred)
3. **Indexing** — parses text, headings, links, structured data; stores it in the index
4. **Ranking** — for a query, picks and sorts pages by hundreds of signals: relevance, quality, user behavior, speed, links

A page that isn't in the index won't be found, however good it is.

---

<!-- Slide 6 -->
## Why architecture matters here (link to Module 2)

| Approach | What the bot sees immediately | Risk |
|---|---|---|
| **SSG / SSR** | Ready HTML with content | Minimal |
| **SPA** | An empty `<div id="root">` | Content shows up only after rendering — later, and not always |

The "Slot" public page is SSR/SSG. The admin panel is an SPA and doesn't need indexing at all (`noindex`).

---

<!-- Slide 7 -->
## Technical SEO: a checklist

- `robots.txt` — what may be crawled; `sitemap.xml` — the list of pages
- `<title>` and `<meta name="description">` — unique for every page
- `<link rel="canonical">` — the main version when there are duplicates
- One `<h1>`, a logical heading hierarchy
- Human-readable URLs: `/beard-barbershop/services`, not `/?id=17`
- **Mobile-first**: the mobile version is what gets indexed
- HTTPS, fast loading (Core Web Vitals)

---

<!-- Slide 8 -->
## Open Graph and structured data

```html
<meta property="og:title" content="Beard Barbershop — book online">
<meta property="og:image" content="https://slot.example/og/beard.png">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HairSalon",
  "name": "Beard Barbershop",
  "address": { "@type": "PostalAddress", "addressLocality": "Kazan" },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "128" }
}
</script>
```

- **Open Graph** — how a link looks in Telegram, VK, social networks
- **schema.org (JSON-LD)** — the search engine understands what the entity is; a chance at a rich snippet

---

<!-- Slide 9 -->
## Google and Yandex

| | Google | Yandex |
|---|---|---|
| Console | Search Console | Yandex Webmaster |
| Specifics | Stronger link signals, Core Web Vitals | Stronger behavioral factors, regionality, commercial factors |
| Local business | Google Business Profile | Yandex Business, Yandex Maps |

For "Slot" in Russia: **Yandex Business** and Maps are a must — people search for "barbershop near me".

---

<!-- Slide 10 -->
## Content SEO

- **Search intent:** what does the person want — to learn, to buy, to find a place?
- Key phrases: Yandex Wordstat, Google Keyword Planner — what and how much people search
- **A landing page per scenario:** "beard trim Kazan", "book a barber online"
- Useful content beats "text for the robot": prices, photos of work, reviews
- **Links** from other sites — recommendations the search engine trusts
- Don't buy from "guaranteed SEO promoters": purchased links get penalized

---

<!-- Slide 11 -->
## How social media feeds rank

A feed is a recommender system: it predicts what you'll watch to the end and interact with.

| Signal | Why it matters |
|---|---|
| **Watch time, completions** | The main interest signal for short video |
| **Saves, shares** | Stronger than likes: "this is valuable" |
| **Comments** | Engagement, discussion |
| **Early velocity** | A post is tested on a small audience; if it lands → it's shown wider |
| **Skips, hides** | A negative signal |

---

<!-- Slide 12 -->
## Interest graph vs social graph

| | Social graph | Interest graph |
|---|---|---|
| Who sees it | Your followers and friends | Anyone the topic might interest |
| Examples | Classic VK and Facebook feeds | TikTok, YouTube Shorts, Reels, Dzen |
| What it means for a newcomer | You need a follower base | A chance at reach from zero |

For a launch with no audience — **interest-graph** formats: short video, Shorts.

---

<!-- Slide 13 -->
## Launch channels

| Channel | Who it fits |
|---|---|
| **Telegram** — your own and topical channels, chats | Almost everyone in Russia |
| **VK** — communities, geo-targeted ads | Local business, B2C |
| **YouTube Shorts, TikTok, Reels** | Visual products, "before/after" |
| **Habr, VC.ru** | Developers, entrepreneurs, B2B |
| **Product Hunt, Reddit, Hacker News** | An international technical audience |
| **Local communities, offline** | A QR code at the barbershop counter is a channel too |

Rule: **1–2 channels where your audience definitely is** beat 10 "just to tick the box".

---

<!-- Slide 14 -->
## Positioning and the landing page

- **One audience:** solo barbers and tutors, not "everyone who works with clients"
- **One problem:** "clients message at night, bookings get lost"
- **One promise:** "booking without chatting, in 30 seconds"
- **One call to action:** "Connect for free"
- Proof: screenshots, reviews from the first masters, numbers

If a landing page can't be retold in one sentence, it won't be understood.

---

<!-- Slide 15 -->
## The AARRR funnel

| Stage | Question | "Slot" metric |
|---|---|---|
| **Acquisition** | Where did they come from? | Visitors per channel |
| **Activation** | Did they get value? | A master published a schedule |
| **Retention** | Did they come back? | A master is active after 4 weeks |
| **Referral** | Did they bring others? | Clients → new masters |
| **Revenue** | Do they pay? | Upgrade to a paid plan |

Fix the leakiest stage of the funnel, not the most interesting one.

---

<!-- Slide 16 -->
## Analytics

- **Yandex Metrica** — goals, Webvisor (session recordings), click maps; popular in Russia
- **GA4** — events, funnels, Google Ads integration
- **Product analytics** — PostHog, Amplitude: behavior inside the app
- **Goals / events:** `booking_created`, `master_signed_up` — sent from code
- **UTM tags** — where a person came from:

```
https://slot.example/?utm_source=telegram&utm_medium=post&utm_campaign=launch
```

---

<!-- Slide 17 -->
## Privacy and consent

- Analytics and cookies collect **personal data**
- You need: a privacy policy, a consent banner for non-essential cookies
- In Russia — **Federal Law 152-FZ**: consent to processing, storing Russian citizens' data on servers in Russia, notifying Roskomnadzor
- In the EU — GDPR: explicit consent before setting analytics cookies
- Collect only what you actually use

Not legal advice — for a real business, check with a lawyer.

---

<!-- Slide 18 -->
## Promotion and AI agents

- An agent is a good **technical SEO auditor**: it checks meta tags, sitemap, structured data, headings
- An agent quickly drafts **posts and headline variants** for A/B tests
- But: templated AI text gets recognized and down-ranked by algorithms and people — **rewrite it in your own voice**
- AI search answers (AI Overviews, Yandex Neuro) also rely on clear, structured content and markup

---

<!-- Slide 19 -->
## Lab

1. Make "Slot" indexable: `robots.txt`, `sitemap.xml`, title/description, OG, JSON-LD
2. Add the site to Yandex Webmaster and Google Search Console
3. Set up analytics with a "booking created" goal and UTM tags
4. Write a one-sentence positioning and update the landing page
5. A launch plan for **two** channels: content, dates, target metrics
6. **With an agent:** ask the agent for a technical SEO audit of the public page and draft posts; rewrite the posts in your own voice

---

<!-- Slide 20 -->
## Deliverable

- A passed SEO checklist (Lighthouse SEO + a structured-data validator)
- An analytics dashboard with goals
- A launch plan: channels, content, dates, AARRR target metrics
- Which parts of the agent's audit were useful and which were noise

---

<!-- Slide 21 -->
## Recap and next module

- Search: crawl → render → index → rank; SSR/SSG help
- Feeds are recommender systems: watch time, saves, the first hours
- 1–2 channels where your audience is; one promise on the landing page
- Measure the funnel and fix the weakest stage
- Next: **Module 13 — Capstone**: launching all of "Slot"
