# 67858.com — Phase-wise Build Prompts

Idea: **67858.com — Number & Money Lab.** A free hub of money, business, website and AI calculators plus a "Number Lab" that decodes any number (maths, cultural symbolism, memorability). Monetized by Google AdSense (Auto ads), lead generation (free Growth & Funding Plan), sponsorships, contests and reader support. Static HTML, hosted free on GitHub Pages.

Global rules for every phase (paste at the top of each prompt):
- Static HTML/CSS/vanilla JS only; must run on GitHub Pages free plan (no server, no build step at deploy).
- Every page `<head>` includes: `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>`
- Every page top bar: "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" → https://web.works/contact
- One inbox for every form and contact link. The address must never appear in HTML or as plain text in JS: store it as shifted char codes and assemble it only at click/submit time (FormSubmit AJAX endpoint, mailto, PayPal donate).
- No use of "67858" as a claimed trademark; include a trademark & copyright disclosure page and footer notice.
- AdSense compliance: original content, no ad-like placeholders, no "click ads" language, About/Contact/Privacy/Terms/Disclaimer pages, ads.txt, cookie notice, Google-certified CMP for EEA/UK.

---

## Phase 1 — Research & positioning
> Research the number 67858 / "678 58" across commerce, business, AI, economy and culture. Report: postal/area-code collisions, part-number collisions, Chinese digit homophones (6 smooth, 8 prosper, 58 "I prosper", 678 rising run), the 2025 "6-7" Word of the Year meme, and search-demand angles. Then survey 25+ leading calculator, finance-tool and number-meaning websites and list: signature tools, forms, content types, UX patterns, monetization and trust signals. Output a ranked must-have feature list and an AdSense-approval checklist. Recommend one site concept with revenue math (ads + leads + sponsors + donations).

## Phase 2 — Information architecture & design system
> Design the sitemap: Home, Calculators hub (4 categories), 30+ calculator pages, Number Lab, Guides hub + 10 guides, Video library, Free Growth Plan (lead funnel), Support/Donate, Contests, Careers, Advertise/Partner, Contact, About, Editorial policy, Glossary, Privacy, Terms, Disclaimer, Trademark, 404. Create a CSS design system: ink/gold/teal palette, Sora + Inter + JetBrains Mono, light/dark themes via tokens, cards, chips, buttons, forms, result cards, sticky sidebar, mobile-first with no horizontal scroll at 360px. Write a Python generator (src/build.py) that renders every page from shared header/footer templates with relative links.

## Phase 3 — Calculator engine + 34 calculators
> Build assets/js/calc.js: generic engine that reads `data-k` inputs, calls a per-page `compute(v)` returning `{results, series, steps}`, renders result cards and an inline SVG stacked bar chart, supports currency symbol switching, shareable URLs that reload inputs, copy/print, recent-calculation history in localStorage and a "was this helpful" vote. Define 34 calculators in src/calcs.py across Money & Loans, Business & Pricing, Websites/Creators & AI, Everyday Numbers. Each page: H1, byline + updated date, tool above the fold, quick answer, how-to steps, formula, worked example (generated from the same formula and verified), FAQs, assumptions/limits, related tools, lead form in the sidebar, JSON-LD (SoftwareApplication, FAQPage, BreadcrumbList). Unit-test every formula with default inputs in Node.

## Phase 4 — Number Lab
> Build number-lab.html + assets/js/numberlab.js: input any number (≤15 digits), show words, parity, primality, prime factorisation, digit sum, reverse, square root, binary, hex, Roman; a transparent 1–99 memorability score (length, distinct digits, repeats, palindrome, sequences, halves, 8/6/4 preferences); digit-by-digit Chinese homophone meanings and known combos (168, 518, 58, 88, 888, 666, 520, 1314, 67, 678); Pythagorean numerology reduction. Frame all symbolism as tradition/entertainment. Support `?n=` deep links and quick-try chips.

## Phase 5 — Content & video
> Write 10 original guides (600–900 words) with worked numbers: What does 6-7 mean; Lucky numbers in business; Compound interest; Break-even; Margin vs markup; Website earnings math; AI costs for small business; Startup runway; Unit economics; Domain investing by the numbers. Article schema, breadcrumbs, related tools, sources & methodology note. Build a video library with click-to-load YouTube facades (youtube-nocookie) using only verified video IDs, plus curated YouTube search links and a creator-submission CTA.

## Phase 6 — Lead generation (highest priority for revenue)
> Build get-a-plan.html: 5-step funnel (goal → stage → revenue → budget/timeline → contact) with progress bar, auto-advance on radio selection, validation per step, consent + optional partner-matching opt-in, trust row. Add an inline lead form on every calculator and guide that attaches the user's calculation to the submission, a sticky CTA after scroll and a once-per-session desktop exit-intent modal (never on the funnel page). Footer newsletter on every page. All forms POST via FormSubmit AJAX to the hidden inbox, with honeypot spam protection.

## Phase 7 — Donations, contests, hiring, sponsorship
> support.html: 4 tiers + custom amount → PayPal donate (address assembled at click), purpose allocation (operations, marketing, hiring, prizes), sponsor-a-prize/in-kind pledge form. contests.html: monthly "Number Crunch" challenge, prize pool, entry form with 18+ and rules acceptance, official rules (no purchase necessary, skill-based, void where prohibited). careers.html: 6 remote roles + application form. advertise.html: 6 sponsorship packages, media-kit form, domain/partnership CTA to web.works/contact, ad standards.

## Phase 8 — Trust, legal & AdSense readiness
> About, Editorial policy, Privacy (Google advertising cookie disclosure + opt-out links, GDPR/CCPA/PIPEDA/Law 25 rights), Terms, Disclaimer, Trademark & copyright disclosure, Glossary (DefinedTermSet). ads.txt `google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`, robots.txt, sitemap.xml, webmanifest, favicon, OG image, canonical URLs to https://67858.com/, .nojekyll, 404.

## Phase 9 — QA
> Run the generator; run every calculator compute in Node; headless-browser screenshots at 1366px and 390px; assert no JS errors and no horizontal overflow; grep the output to confirm the inbox address never appears in any file; validate internal links.

## Phase 10 — Deploy & launch
> Push to GitHub WEBWORKSA1/67858-com (main). Enable GitHub Pages from main / root. Point 67858.com DNS to GitHub Pages (A records 185.199.108.153, .109.153, .110.153, .111.153; CNAME www → webworksa1.github.io), add the custom domain in Settings → Pages, enforce HTTPS. Submit sitemap in Google Search Console, then apply in AdSense with 67858.com, enable Auto ads and the Google-certified CMP. Send one test submission to activate FormSubmit.

## Phase 11 — Growth roadmap
> Monthly: 4 new calculators, 4 guides, 1 contest. Add programmatic but substantive pages for high-demand numbers only after traffic proves demand; add embeddable calculator widgets for backlinks; add manual AdSense units (below results, in-article, sticky sidebar) once slot IDs exist; A/B test funnel copy; sell lead partnerships by category.
