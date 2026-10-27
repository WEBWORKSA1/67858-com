# 67858.com — Number & Money Lab

Free money, business, website & AI calculators, a Number Lab that decodes any number, guides, a video library, a lead-generation funnel, contests, donations, careers and sponsorships. Static HTML + a shared Jekyll layout — GitHub Pages (free plan) builds and hosts it with no extra setup.

## Research summary (why this idea)
- **No collisions:** 67858 is not an active US ZIP (neighbours 67857/67859 are Kansas); only incidental part-number uses exist. Clean, brandable numeric .com.
- **Built-in story:** 678 = rising run; 58 is read in Chinese number culture as "I prosper"; 6 ≈ "smooth", 8 ≈ "prosper". Starts with **67** — the "6-7" meme Dictionary.com named 2025 Word of the Year.
- **Revenue logic:** Numeric domains fit tools, not brands-of-a-thing. Calculator sites are evergreen search magnets; finance/business topics carry some of the highest AdSense RPMs; calculator users are mid-decision, which makes lead capture convert.
- **Revenue stack:** AdSense Auto ads + opt-in leads (funding, pricing, web/AI build, domain/site deals) + labelled sponsorships + contest sponsors + reader support.
- Benchmarked against 25 sites (calculator.net, Omni, CalculatorSoup, Bankrate, SmartAsset, RapidTables, TheCalculatorSite, Financial Mentor, HubSpot tools, Shopify tools, Wise, Xe, Sleep Foundation, Numerologist, Wolfram|Alpha, Ramsey, MortgageCalculator.org, Dinkytown, Forbes Advisor, InchCalculator, Astrology.com and others).

## Structure
```
index.html, calculators.html, number-lab.html, guides.html, videos.html,
get-a-plan.html (lead funnel), support.html (donate), contests.html, careers.html,
advertise.html, contact.html, about.html, editorial-policy.html, glossary.html,
privacy.html, terms.html, disclaimer.html, trademark.html, 404.html
calculators/*.html (34)   guides/*.html (10)
assets/css/style.css   assets/js/{main,calc,numberlab}.js   assets/img/
_layouts/default.html (shared head/top bar/nav/footer, AdSense script)
ads.txt robots.txt sitemap.xml site.webmanifest CNAME _config.yml
src/ — generator (build.py), calculator definitions (calcs.py), guides (guides.py), main.js template
PROMPTS.md — phase-wise build prompts
```

## Edit & rebuild
```
python3 src/build.py
```
Add a calculator: append an `add(...)` block in `src/calcs.py`. Add a guide: append to `src/guides.py`. Rebuild, commit, push.

## Go-live checklist
1. **GitHub Pages:** currently live from the `gh-pages` branch. To make every push to `main` deploy automatically, set Settings → Pages → Deploy from branch → `main` / `(root)` (then `gh-pages` can be deleted).
2. **Custom domain:** `CNAME` contains `67858.com`; DNS A records already point to GitHub Pages (185.199.108–111.153). In Settings → Pages confirm the custom domain and tick **Enforce HTTPS**.
3. **Forms:** submit any form once; FormSubmit sends a one-time activation email to the site inbox — click it. All forms then deliver there.
4. **Donations:** PayPal donate links use the same inbox; it must be a PayPal-registered email.
5. **AdSense:** add `67858.com` in AdSense, keep Auto ads on, enable the Google-certified CMP (Privacy & messaging) for EEA/UK. `ads.txt` is already in place.
6. **Search Console:** verify the domain and submit `https://67858.com/sitemap.xml`.

## Compliance
- Contact inbox never appears in markup; it is assembled at click/submit time.
- Trademark & copyright disclosure: `/trademark.html` + footer notice.
- All calculators: formula, worked example, assumptions, "not advice" notice, updated date.
