#!/usr/bin/env python3
"""Static site generator for 67858.com — run `python3 src/build.py` from the repo root.
Outputs plain HTML into the repo root so GitHub Pages (free plan) serves it with no build step."""
import os, json, html, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from calcs import C as CALCS, CATS
from guides import G as GUIDES

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = "https://67858.com/"
NAME = "67858.com"
TAG = "Number & Money Lab"
UPDATED = "October 27, 2026"
ISO = "2026-10-27"
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
INTEREST = "https://web.works/contact"
VIDEOS = [
    ("Rm6UdfRs3gw", "Compound interest introduction", "Khan Academy", "Money"),
    ("wf91rEGw88Q", "What Is Compound Interest?", "Investopedia", "Money"),
    ("PHe0bXAIuk0", "How The Economic Machine Works", "Principles by Ray Dalio", "Economy"),
    ("3ez10ADR_gM", "Intro to Economics: Crash Course Econ #1", "CrashCourse", "Economy"),
    ("aircAruvnKk", "But what is a neural network?", "3Blue1Brown", "AI"),
    ("LPZh9BOjkQs", "Large Language Models explained briefly", "3Blue1Brown", "AI"),
]
CAL = {c['slug']: c for c in CALCS}
esc = html.escape

def email_codes():
    # Contact inbox stored only as shifted character codes (never plain text anywhere in the repo)
    return "[126, 108, 105, 126, 118, 121, 114, 122, 104, 56, 71, 110, 116, 104, 112, 115, 53, 106, 118, 116]"

NAV = [("calculators.html","Calculators"),("number-lab.html","Number Lab"),("guides.html","Guides"),("videos.html","Videos"),("contests.html","Contests"),("support.html","Support Us")]

JEKYLL = True  # emit pages that share _layouts/default.html (GitHub Pages builds them for free)

def page(path, title, desc, body, active="", extra_head="", scripts="", schema=None, body_attr="", r=None):
    depth = path.count('/')
    r = ("../" * depth) if r is None else r
    canon = SITE + ("" if path == "index.html" else path)
    ld = ""
    for s in (schema or []):
        ld += f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>\n'
    full_title = title if NAME in title else f"{title} | {NAME}"
    if JEKYLL:
        fm = {"layout":"default","title":title,"full_title":full_title,"description":desc,"canonical":canon,"r":r,"active":active}
        if body_attr: fm["nocta"] = True
        if path == "404.html": fm["permalink"] = "/404.html"
        front = "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k,v in fm.items()) + "---\n"
        return front + "{% raw %}" + ld + body + scripts + "{% endraw %}\n"
    menu = "".join(f'<li><a href="{r}{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a></li>' for h,t in NAV)
    return tmpl(r, full_title, desc, canon, title, menu, ld, body, scripts, body_attr, esc_on=True)

def layout_html():
    menu = "".join(f'<li><a href="{{{{ page.r }}}}{h}"{{% if page.active == "{h}" %}} aria-current="page"{{% endif %}}>{t}</a></li>' for h,t in NAV)
    return tmpl("{{ page.r }}", "{{ page.full_title | escape }}", "{{ page.description | escape }}", "{{ page.canonical }}", "{{ page.title | escape }}", menu, "", "{{ content }}", "", "{% if page.nocta %} data-nocta{% endif %}", esc_on=False)

def tmpl(r, full_title, desc, canon, title, menu, ld, body, scripts, body_attr, esc_on=True):
    e = esc if esc_on else (lambda x: x)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0d1321">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{r}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{r}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&family=Sora:wght@700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css">
{ADS}
{ld}
</head>
<body{body_attr}>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><a href="{INTEREST}" target="_blank" rel="noopener">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership</a></div>
<header class="site-head"><div class="wrap nav">
<a class="brand" href="{r}index.html" aria-label="{NAME} home"><span class="logo">678<br>58</span><span>{NAME}<small>{TAG}</small></span></a>
<ul class="menu" id="menu">{menu}<li><a class="cta" href="{r}get-a-plan.html">Free Growth Plan</a></li></ul>
<button class="icon-btn burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu">☰</button>
<button class="icon-btn" id="themeBtn" aria-label="Toggle dark mode">◐</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div class="foot-grid">
<div><a class="brand" href="{r}index.html" style="color:#fff"><span class="logo">678<br>58</span><span>{NAME}<small style="color:#9aa3b5">{TAG}</small></span></a>
<p style="margin-top:14px;font-size:.92rem">Free calculators, number intelligence and plain-English guides that help people and businesses make better money decisions.</p>
<form data-form="Newsletter" data-ok="You're in. Watch your inbox for the weekly Numbers Brief." style="display:flex;gap:8px;flex-wrap:wrap">
<div class="hp"><input name="_honey" tabindex="-1" autocomplete="off"></div>
<input type="email" name="email" required placeholder="Email for the weekly Numbers Brief" aria-label="Email" style="flex:1;min-width:180px;padding:10px 12px;border-radius:10px;border:1px solid #2a3348;background:#111827;color:#fff">
<button class="btn btn-gold" type="submit" style="padding:10px 14px">Subscribe</button><p class="form-msg" style="width:100%;margin:0"></p></form></div>
<div><h4>Tools</h4><ul><li><a href="{r}calculators.html">All calculators</a></li><li><a href="{r}calculators.html#money">Money & loans</a></li><li><a href="{r}calculators.html#business">Business</a></li><li><a href="{r}calculators.html#web-ai">Websites & AI</a></li><li><a href="{r}number-lab.html">Number Lab</a></li></ul></div>
<div><h4>Learn</h4><ul><li><a href="{r}guides.html">Guides</a></li><li><a href="{r}videos.html">Video library</a></li><li><a href="{r}glossary.html">Glossary</a></li><li><a href="{r}guides/what-does-6-7-mean.html">What does 6-7 mean?</a></li></ul></div>
<div><h4>Get involved</h4><ul><li><a href="{r}get-a-plan.html">Free growth plan</a></li><li><a href="{r}contests.html">Contests & prizes</a></li><li><a href="{r}support.html">Support / donate</a></li><li><a href="{r}careers.html">Careers & talent</a></li><li><a href="{r}advertise.html">Advertise & sponsor</a></li></ul></div>
<div><h4>Company</h4><ul><li><a href="{r}about.html">About</a></li><li><a href="{r}contact.html">Contact</a></li><li><a href="{r}editorial-policy.html">Editorial policy</a></li><li><a href="{r}privacy.html">Privacy</a></li><li><a href="{r}terms.html">Terms</a></li><li><a href="{r}disclaimer.html">Disclaimer</a></li><li><a href="{r}trademark.html">Trademark & copyright</a></li></ul></div>
</div>
<div class="legal">© <span data-year>2026</span> {NAME}. All rights reserved. Calculators and content are for educational purposes and are not financial, legal or tax advice. “67858” is used solely as this website's domain name and carries no claim to, or affiliation with, any third-party mark, product number, postal code or person. See our <a href="{r}trademark.html">trademark & copyright disclosure</a>. · <a href="{INTEREST}" target="_blank" rel="noopener">Interested in this domain or a partnership?</a></div>
</div></footer>
<div class="consent" id="consent" role="dialog" aria-label="Cookie notice"><p>We use cookies for essential site functions and, with Google AdSense, to show and measure ads. See our <a href="{r}privacy.html">privacy policy</a>.</p><button class="btn btn-ghost" data-consent="essential">Essential only</button><button class="btn btn-teal" data-consent="all">Accept all</button></div>
<a class="btn btn-gold sticky-cta" id="stickyCta" href="{r}get-a-plan.html">📈 Get my free growth plan</a>
<div class="modal" id="exitModal" role="dialog" aria-label="Free growth plan offer"><div class="card"><button class="x" aria-label="Close">×</button><span class="tag">Before you go</span><h3>Get a free, personalised growth & funding plan</h3><p>Answer 5 quick questions and get a plan built around your numbers — revenue, costs and goals. No cost, no obligation.</p><p style="margin-top:14px"><a class="btn btn-teal btn-block" href="{r}get-a-plan.html">Start my free plan →</a></p></div></div>
<script src="{r}assets/js/main.js" defer></script>
{scripts}
</body>
</html>
"""

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

def hp():
    return '<div class="hp"><input name="_honey" tabindex="-1" autocomplete="off"></div>'

def consent_box(txt="I agree to be contacted about my request and accept the privacy policy."):
    return f'<label class="check"><input type="checkbox" name="consent" value="yes" required> <span>{txt}</span></label>'

def calc_card(c, r):
    return f'<a class="card" href="{r}calculators/{c["slug"]}.html" data-cat="{c["cat"]}" data-name="{esc(c["title"].lower()+" "+c["short"].lower())}"><div class="ico">{c["icon"]}</div><h3>{esc(c["title"])}</h3><p>{esc(c["short"])}</p></a>'

def guide_card(g, r):
    return f'<a class="card" href="{r}guides/{g["slug"]}.html"><span class="tag">{esc(g["cat"])}</span><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p><p class="muted" style="margin-top:8px;font-size:.82rem">{g["read"]} min read</p></a>'

def video_card(v):
    vid, t, a, cat = v
    return f'<div class="card"><div class="video" data-yt="{vid}" data-title="{esc(t)}" role="button" tabindex="0" aria-label="Play: {esc(t)}"><img loading="lazy" src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="{esc(t)} — video thumbnail" width="480" height="360"><div class="play"><i>▶</i></div></div><span class="tag" style="margin-top:12px">{cat}</span><h3>{esc(t)}</h3><p>By {esc(a)} · via YouTube</p></div>'

def breadcrumb(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+u} for i,(n,u) in enumerate(items)]}

INCLUDES = {}
def inc(name, static_html, liquid_html=None, **params):
    """Shared block: inline in standalone mode, Jekyll include in JEKYLL mode (keeps the repo small)."""
    if not JEKYLL: return static_html
    INCLUDES[name] = liquid_html if liquid_html is not None else static_html
    ps = "".join(f' {k}="{v}"' for k,v in params.items())
    return "{% endraw %}{% include " + name + ps + " %}{% raw %}"

def lead_inline(source, r, title="Want a plan built on these numbers?", sub="Get a free, personalised growth & funding plan from our team — based on your actual figures. Reply within 1–2 business days."):
    return inc("lead.html", _lead(source, title, sub), _lead("{{ include.source }}", "{{ include.title }}", "{{ include.sub }}", raw=True), source=source, title=title, sub=sub)

def _lead(source, title, sub, raw=False):
    e = (lambda x: x) if raw else esc
    return f'''<div class="card" id="lead"><span class="tag">Free · no obligation</span><h3>{title}</h3><p>{sub}</p>
<form data-form="Lead — {e(source)}" id="resultLead" style="margin-top:12px">{hp()}<input type="hidden" name="source" value="{e(source)}"><input type="hidden" name="calculation" value="">
<div class="f"><label for="ln-{source}">Name</label><input id="ln-{source}" name="name" required autocomplete="name"></div>
<div class="f"><label for="le-{source}">Email</label><input id="le-{source}" type="email" name="email" required autocomplete="email"></div>
<div class="f"><label for="lg-{source}">I want help with</label><select id="lg-{source}" name="goal"><option>Business funding / loans</option><option>Growing revenue & pricing</option><option>Building a website or AI tool</option><option>Buying or selling a website/domain</option><option>Personal finance planning</option></select></div>
{consent_box()}<button class="btn btn-teal btn-block" type="submit">Send me my free plan</button><p class="form-msg"></p></form></div>'''


# ---- shared calculator blocks (become Jekyll includes) ----
CALC_OUT = '<div class="field"><label for="curSel">Currency symbol</label><div class="inp"><select id="curSel"><option>$</option><option>€</option><option>£</option><option>₹</option><option>¥</option><option>C$</option><option>A$</option></select></div></div>\n</form>\n<div class="calc-out" aria-live="polite"><div class="results" id="results"></div><div class="chart" id="chart" style="display:none"></div><p id="steps" style="color:#b9c0cf;font-size:.88rem;margin:12px 0 0"></p>\n<div class="calc-actions"><button class="btn btn-gold" id="btnShare" type="button">🔗 Share result</button><button class="btn btn-ghost" style="color:#fff!important;border-color:#2a3348" id="btnCopy" type="button">Copy</button><button class="btn btn-ghost" style="color:#fff!important;border-color:#2a3348" id="btnPrint" type="button">Print</button><a class="btn btn-teal" href="#lead">Get a free plan →</a></div></div></div>'
HOWTO = '<h2>How to use the @@T@@</h2>\n<ol><li>Enter your figures in the fields above — results update instantly as you type.</li><li>Choose your currency symbol (the maths is the same in any currency).</li><li>Use <em>Share result</em> to save a link that reloads your exact inputs, or <em>Print</em> for your records.</li><li>Compare scenarios by changing one input at a time and noting how the main result moves.</li></ol>\n'
LIMITS = '<h2>Assumptions & limits</h2><p>Results are estimates based on the inputs you provide and the formula shown, rounded for display. They do not account for every fee, tax rule or market condition. This tool is educational and is not financial, tax or legal advice — confirm important decisions with a qualified professional.</p>\n<div id="voteWrap" class="card" style="margin-top:18px"><strong>Was this calculator helpful?</strong> <button class="chip" data-vote="yes">👍 Yes</button> <button class="chip" data-vote="no">👎 Not really</button></div>'
SIDE = '<div class="card"><span class="tag">Number Lab</span><h3>Check any number</h3><p>Score a phone number, price or domain for memorability and symbolism.</p><p style="margin-top:10px"><a class="btn btn-ghost btn-block" href="@@R@@number-lab.html">Open Number Lab</a></p></div>\n<div class="card"><span class="tag">Support</span><h3>Keep these tools free</h3><p>Reader support funds new calculators and monthly prizes.</p><p style="margin-top:10px"><a class="btn btn-gold btn-block" href="@@R@@support.html">Support 67858.com</a></p></div>\n'
# ---------------- Calculator pages ----------------
def render_inputs(c):
    out = []
    for inp in c["inputs"]:
        k, label, d, pre, suf, step, hint = inp
        if pre == "select":
            opts = "".join(f'<option value="{v}"{" selected" if str(v)==str(d) else ""}>{esc(l)}</option>' for v,l in suf)
            out.append(f'<div class="field"><label for="i-{k}">{esc(label)}</label><div class="inp"><select id="i-{k}" data-k="{k}">{opts}</select></div>{f"<small>{esc(hint)}</small>" if hint else ""}</div>')
        else:
            p = '<span class="cur">$</span>' if pre == "cur" else (f"<span>{pre}</span>" if pre else "")
            s = f"<span>{esc(suf)}</span>" if suf else ""
            out.append(f'<div class="field"><label for="i-{k}">{esc(label)}</label><div class="inp">{p}<input id="i-{k}" data-k="{k}" type="number" inputmode="decimal" step="{step}" value="{d}">{s}</div>{f"<small>{esc(hint)}</small>" if hint else ""}</div>')
    return "".join(out)

def build_calc(c):
    r = "../"
    catname = CATS[c["cat"]][0]
    related = [x for x in CALCS if x["cat"] == c["cat"] and x["slug"] != c["slug"]][:6]
    gl = [g for g in GUIDES if c["slug"] in g["related"]]
    faqs = "".join(f'<details class="faq"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q,a in c["faqs"])
    body = f'''<div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="{r}index.html">Home</a> › <a href="{r}calculators.html">Calculators</a> › <a href="{r}calculators.html#{c["cat"]}">{catname}</a> › {esc(c["title"])}</nav>
<div class="calc-layout"><div>
<h1 style="font-size:clamp(1.7rem,3.4vw,2.5rem)">{esc(c["title"])}</h1>
<div class="meta"><span>✔ Reviewed by the {NAME} editorial team</span><span>Updated {UPDATED}</span><span><a href="{r}editorial-policy.html">Methodology</a></span></div>
<p class="muted">{esc(c["short"])}</p>
<div class="calc"><form id="calcForm" class="calc-in" novalidate>{render_inputs(c)}
{inc("calc-out.html", CALC_OUT)}
<div class="prose" style="margin-top:32px">
<div class="callout"><strong>Quick answer:</strong> {esc(c["intro"])}</div>
{inc("calc-howto.html", HOWTO.replace("@@T@@", esc(c["title"])), HOWTO.replace("@@T@@", "{{ include.title }}"), title=esc(c["title"]))}<h2>Formula</h2><span class="formula">{esc(c["formula"])}</span>
<h2>Worked example</h2><p>{esc(c["example"])}</p>
<h2>Frequently asked questions</h2>{faqs}
{"<h2>Learn more</h2><ul>"+"".join(f'<li><a href="{r}guides/{g["slug"]}.html">{esc(g["title"])}</a></li>' for g in gl)+"</ul>" if gl else ""}
{inc("calc-limits.html", LIMITS)}
</div>
<section style="padding:36px 0 0"><h2>Related calculators</h2><div class="grid g3">{"".join(calc_card(x, r) for x in related)}</div></section>
</div>
<aside class="side">{lead_inline(c["slug"], r)}
{inc("calc-side.html", SIDE.replace("@@R@@", r), SIDE.replace("@@R@@", "{{ page.r }}"))}</aside></div></div>'''
    schema = [
        {"@context":"https://schema.org","@type":"SoftwareApplication","name":c["title"],"applicationCategory":"FinanceApplication","operatingSystem":"Any (web browser)","url":SITE+"calculators/"+c["slug"]+".html","description":c["short"],"offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"dateModified":ISO},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c["faqs"]]},
        breadcrumb([("Home",""),("Calculators","calculators.html"),(c["title"],"calculators/"+c["slug"]+".html")])]
    js_obj = f'<script>window.CALC={{id:{json.dumps(c["slug"])},title:{json.dumps(c["title"], ensure_ascii=False)},compute:function(v){{{c["js"]}}}}};</script><script src="{r}assets/js/calc.js" defer></script>'
    write(f'calculators/{c["slug"]}.html', page(f'calculators/{c["slug"]}.html', f'{c["title"]} — Free & Instant', c["short"]+" Free, instant, with formula, worked example and FAQs.", body, "calculators.html", scripts=js_obj, schema=schema))

# ---------------- Guides ----------------
def build_guide(g):
    r = "../"
    rel = [CAL[s] for s in g["related"] if s in CAL]
    others = [x for x in GUIDES if x["slug"] != g["slug"]][:3]
    body = f'''<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{r}index.html">Home</a> › <a href="{r}guides.html">Guides</a> › {esc(g["title"])}</nav>
<div class="calc-layout"><article class="prose">
<span class="tag" style="display:inline-block;margin-top:14px;font:600 .72rem var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--teal-d)">{esc(g["cat"])}</span>
<h1 style="font-size:clamp(1.8rem,3.6vw,2.7rem)">{esc(g["title"])}</h1>
<div class="meta"><span>By the {NAME} editorial team</span><span>Updated {UPDATED}</span><span>{g["read"]} min read</span></div>
<p class="muted" style="font-size:1.1rem">{esc(g["desc"])}</p>
{g["body"]}
<div class="card" style="margin-top:28px"><strong>Sources & methodology.</strong> <span class="muted">Figures in this guide are computed with the formulas shown and our open calculators. Cultural and historical references are summarised from public reporting and reference works; see our <a href="{r}editorial-policy.html">editorial policy</a>. Educational content, not personal financial advice.</span></div>
<section style="padding:32px 0 0"><h2>Keep reading</h2><div class="grid g3">{"".join(guide_card(x, r) for x in others)}</div></section>
</article>
<aside class="side"><div class="card"><span class="tag">Try it</span><h3>Tools for this guide</h3><ul style="padding-left:18px;margin:0">{"".join(f'<li><a href="{r}calculators/{c["slug"]}.html">{esc(c["title"])}</a></li>' for c in rel)}</ul></div>
{lead_inline(g["slug"], r)}</aside></div></div>'''
    schema = [{"@context":"https://schema.org","@type":"Article","headline":g["title"],"description":g["desc"],"dateModified":ISO,"datePublished":ISO,"author":{"@type":"Organization","name":NAME+" editorial team"},"publisher":{"@type":"Organization","name":NAME,"logo":{"@type":"ImageObject","url":SITE+"assets/img/favicon.svg"}},"mainEntityOfPage":SITE+"guides/"+g["slug"]+".html"},
              breadcrumb([("Home",""),("Guides","guides.html"),(g["title"],"guides/"+g["slug"]+".html")])]
    write(f'guides/{g["slug"]}.html', page(f'guides/{g["slug"]}.html', g["title"], g["desc"], body, "guides.html", schema=schema))

# ---------------- Static pages ----------------
def simple(path, title, desc, inner, active="", schema=None, scripts="", body_attr=""):
    write(path, page(path, title, desc, inner, active, schema=schema, scripts=scripts, body_attr=body_attr))

def hero_band(eyebrow, h1, lead, extra=""):
    return f'<section class="hero" style="padding:48px 0 40px"><div class="wrap"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{extra}</div></section>'

def build_home():
    r = ""
    cats = "".join(f'<a class="card" href="calculators.html#{k}"><div class="ico">{v[1]}</div><h3>{v[0]}</h3><p>{v[2]}</p><p style="margin-top:10px;font-weight:600;color:var(--teal-d)">{sum(1 for c in CALCS if c["cat"]==k)} tools →</p></a>' for k,v in CATS.items())
    popular = ["compound-interest-calculator","mortgage-calculator","loan-emi-calculator","break-even-calculator","profit-margin-calculator","ai-token-cost-calculator","adsense-revenue-calculator","percentage-calculator"]
    body = f'''<section class="hero"><div class="wrap hero-grid"><div>
<span class="eyebrow">Free calculators · number intelligence · money guides</span>
<h1>Numbers that move money.</h1>
<p class="lead">{len(CALCS)} instant calculators for loans, business, websites and AI — plus the Number Lab, which decodes any number's maths, symbolism and memorability. Free, private, no sign-up.</p>
<form class="hero-search" id="quickSearch" data-hub="calculators.html" data-lab="number-lab.html" role="search"><input aria-label="Search calculators or enter a number" placeholder="Search “mortgage”… or type any number"><button class="btn btn-gold" type="submit">Go</button></form>
<div class="stats"><div class="stat"><b>{len(CALCS)}</b><small>free calculators</small></div><div class="stat"><b>{len(GUIDES)}</b><small>in-depth guides</small></div><div class="stat"><b>0</b><small>sign-ups required</small></div><div class="stat"><b>100%</b><small>runs in your browser</small></div></div>
</div><div>
<div class="digits" aria-label="6 7 8 5 8"><div class="digit">6<span>SMOOTH</span></div><div class="digit t">7<span>MOMENTUM</span></div><div class="digit g">8<span>PROSPER</span></div><div class="digit">5<span>I / WE</span></div><div class="digit g">8<span>PROSPER</span></div></div>
<p style="color:#9aa3b5;margin-top:14px;font-size:.92rem"><b style="color:#fff">678 · 58</b> — a rising run (6→7→8) followed by “58”, read in Chinese number culture as “I prosper”. Our mission in five digits: help every visitor's numbers climb.</p>
<p><a class="btn btn-teal" href="get-a-plan.html">Get my free growth plan →</a></p>
</div></div></section>

<section><div class="wrap"><div class="section-head"><div><h2>Pick your numbers</h2><p>Four categories, one goal: faster, better money decisions.</p></div><a class="btn btn-ghost" href="calculators.html">All calculators →</a></div>
<div class="grid g4">{cats}</div></div></section>

<section class="alt"><div class="wrap"><div class="section-head"><div><h2>Most-used calculators</h2><p>Instant results, shareable links, formulas and worked examples on every page.</p></div></div>
<div class="grid g4">{"".join(calc_card(CAL[s], r) for s in popular)}</div></div></section>

<section class="band"><div class="wrap hero-grid"><div><span class="eyebrow" style="font:600 .8rem var(--mono);letter-spacing:.12em;color:var(--gold)">NUMBER LAB</span><h2>What does your number say?</h2><p style="color:#b9c0cf">Enter a phone number, price, plate or domain. Get its prime factors, binary and Roman forms, digit symbolism, numerology reduction and a 1–99 memorability score.</p>
<p><a class="btn btn-gold" href="number-lab.html?n=67858">Decode 67858</a> <a class="btn btn-ghost" style="color:#fff!important;border-color:#2a3348" href="number-lab.html?n=67">Try “67”</a></p></div>
<div class="card"><h3 class="mono">67858 at a glance</h3><dl class="kv"><dt>Prime factors</dt><dd>2 × 7 × 37 × 131</dd><dt>Digit sum</dt><dd>34 → reduces to 7</dd><dt>Binary</dt><dd class="mono">10000100100010010</dd><dt>Hex</dt><dd class="mono">10912</dd><dt>In words</dt><dd>sixty-seven thousand eight hundred fifty-eight</dd><dt>Pattern</dt><dd>Starts with the viral “67”; contains 678 and 58</dd></dl></div></div></section>

<section><div class="wrap"><div class="section-head"><div><h2>Guides worth your time</h2><p>Plain-English explainers with real numbers you can check.</p></div><a class="btn btn-ghost" href="guides.html">All guides →</a></div>
<div class="grid g3">{"".join(guide_card(g, r) for g in GUIDES[:6])}</div></div></section>

<section class="alt"><div class="wrap"><div class="grid g2" style="align-items:center"><div><span class="tag" style="display:inline-block;font:600 .72rem var(--mono);color:var(--teal-d);background:rgba(15,157,138,.1);padding:3px 8px;border-radius:6px">Free growth & funding plan</span><h2 style="margin-top:10px">Turn your numbers into a plan</h2><p class="muted">Tell us where your business or project stands. We'll reply with a personalised plan covering pricing, funding options, unit economics and next steps — free and with no obligation.</p>
<ul><li>✔ Reviewed by a human, not a bot</li><li>✔ Funding, pricing, website & AI growth</li><li>✔ Reply within 1–2 business days</li></ul><p><a class="btn btn-teal" href="get-a-plan.html">Start — takes 60 seconds</a></p></div>
<div class="grid g2"><div class="card"><div class="ico">🏆</div><h3>Monthly contests</h3><p>Solve the Number Crunch challenge and win sponsored prizes.</p><p style="margin-top:8px"><a href="contests.html">Enter →</a></p></div><div class="card"><div class="ico">💛</div><h3>Support us</h3><p>Fund new tools, prizes and talent.</p><p style="margin-top:8px"><a href="support.html">Donate →</a></p></div><div class="card"><div class="ico">🧑‍💻</div><h3>Join the team</h3><p>Writers, developers, video creators.</p><p style="margin-top:8px"><a href="careers.html">Careers →</a></p></div><div class="card"><div class="ico">📣</div><h3>Advertise</h3><p>Reach founders and money-minded readers.</p><p style="margin-top:8px"><a href="advertise.html">Sponsor →</a></p></div></div></div></div></section>

<section><div class="wrap"><div class="section-head"><div><h2>Watch & learn</h2><p>Hand-picked lessons on money, economics and AI from leading educators.</p></div><a class="btn btn-ghost" href="videos.html">Video library →</a></div>
<div class="grid g3">{"".join(video_card(v) for v in VIDEOS[:3])}</div></div></section>'''
    schema = [{"@context":"https://schema.org","@type":"WebSite","name":NAME,"url":SITE,"potentialAction":{"@type":"SearchAction","target":SITE+"calculators.html?q={search_term_string}","query-input":"required name=search_term_string"}},
              {"@context":"https://schema.org","@type":"Organization","name":NAME,"url":SITE,"logo":SITE+"assets/img/favicon.svg"}]
    simple("index.html", f"{NAME} — Free Money, Business & AI Calculators + Number Lab", "Free instant calculators for loans, mortgages, margins, break-even, ROI, ad revenue and AI costs, plus a Number Lab that decodes any number. No sign-up.", body, "", schema=schema)

def build_hub():
    sections = ""
    for k,(n,ic,d) in CATS.items():
        sections += f'<section id="{k}" style="padding:28px 0"><h2>{ic} {n}</h2><p class="muted">{d}</p><div class="grid g3">{"".join(calc_card(c, "") for c in CALCS if c["cat"]==k)}</div></section>'
    chips = '<button class="chip on" data-f="all">All</button>' + "".join(f'<button class="chip" data-f="{k}">{v[0]}</button>' for k,v in CATS.items())
    body = hero_band("All tools", "Free calculators", f"{len(CALCS)} calculators with formulas, worked examples and shareable results. Everything runs privately in your browser.") + f'''<div class="wrap" style="padding-top:24px">
<input class="search" id="hubSearch" type="search" placeholder="Search calculators — e.g. loan, margin, AI, tax" aria-label="Search calculators">
<div class="chips" id="hubChips">{chips}</div>
<div id="hubRecent"></div>
{sections}<p id="hubNone" class="muted" style="display:none">No calculator matches that search yet — <a href="contact.html">suggest one</a>.</p></div>'''
    js = '''<script>(function(){var s=document.getElementById('hubSearch'),f='all';
function apply(){var q=s.value.toLowerCase().trim(),any=0;document.querySelectorAll('[data-name]').forEach(function(c){var ok=(f==='all'||c.dataset.cat===f)&&(!q||c.dataset.name.indexOf(q)>-1);c.style.display=ok?'':'none';if(ok)any++});
document.querySelectorAll('main section[id]').forEach(function(sec){sec.style.display=[].some.call(sec.querySelectorAll('[data-name]'),function(c){return c.style.display!=='none'})?'':'none'});document.getElementById('hubNone').style.display=any?'none':'block'}
s.addEventListener('input',apply);document.querySelectorAll('#hubChips .chip').forEach(function(b){b.addEventListener('click',function(){document.querySelectorAll('#hubChips .chip').forEach(function(x){x.classList.remove('on')});b.classList.add('on');f=b.dataset.f;apply()})});
var q=new URLSearchParams(location.search).get('q');if(q){s.value=q;apply()}
try{var h=JSON.parse(localStorage.getItem('h67')||'[]');if(h.length)document.getElementById('hubRecent').innerHTML='<div class="card" style="margin-bottom:10px"><strong>Your recent calculations</strong><ul style="margin:8px 0 0;padding-left:18px">'+h.map(function(x){return '<li><a href="'+x.u+'">'+x.t+'</a> — '+x.r+'</li>'}).join('')+'</ul></div>'}catch(e){}})();</script>'''
    simple("calculators.html", "All Free Calculators — Money, Business, Websites & AI", f"Browse {len(CALCS)} free calculators: loans, mortgages, compound interest, margins, break-even, ROI, CAC/LTV, ad revenue, AI token costs and more.", body, "calculators.html", scripts=js)

def build_lab():
    tries = ["67858","67","678","888","168","518","520","1314","4444","8675309","2026","1234567"]
    body = hero_band("Number Lab", "Decode any number", "Maths, symbolism and memorability for phone numbers, prices, plates, dates and domains — instantly, in your browser.") + f'''<div class="wrap" style="padding-top:28px">
<div class="lab-in"><input id="labNum" inputmode="numeric" aria-label="Enter a number" placeholder="Enter any number" maxlength="20"><button class="btn btn-gold" id="labGo">Decode</button></div>
<div class="chips">{"".join(f'<button class="chip" data-try="{t}">{t}</button>' for t in tries)}</div>
<div id="labOut" aria-live="polite"></div>
<div class="grid g2" style="margin-top:28px"><div class="prose"><h2>How the Number Lab works</h2>
<p><strong>Math profile.</strong> We test primality and factorise numbers up to one trillion by trial division, and convert to words, binary, hexadecimal and Roman numerals.</p>
<p><strong>Memorability score.</strong> A transparent heuristic: shorter numbers, fewer distinct digits, repeats, palindromes, sequential steps and repeating halves raise the score; digits widely avoided in some markets (such as 4) lower it slightly. Use it to compare options side by side, for example when choosing a business phone number or a numeric domain.</p>
<p><strong>Digit symbolism.</strong> Meanings come from well-documented Chinese homophones (8 ≈ “prosper”, 6 ≈ “smooth”, 4 ≈ “death”) and popular number combinations. They are cultural traditions, not predictions.</p>
<p><strong>Numerology.</strong> We show the Pythagorean digit-sum reduction (keeping master numbers 11, 22, 33) with its traditional associations, for interest and entertainment.</p>
<p>Read more: <a href="guides/lucky-numbers-in-business.html">Lucky numbers in business</a> · <a href="guides/what-does-6-7-mean.html">What does 6-7 mean?</a></p></div>
<div>{lead_inline("number-lab", "", "Choosing a number for your brand?", "Domains, phone lines and pricing — get a free plan on picking numbers customers remember.")}</div></div></div>'''
    simple("number-lab.html", "Number Lab — Number Meaning, Lucky Number & Memorability Checker", "Decode any number: prime factors, binary, Roman numerals, Chinese digit symbolism, numerology and a memorability score for phone numbers, prices and domains.", body, "number-lab.html", scripts='<script src="assets/js/numberlab.js" defer></script>')

def build_guides_hub():
    body = hero_band("Guides", "Money & numbers, explained", "Original, plain-English guides with worked examples you can verify in our calculators.") + f'<div class="wrap" style="padding-top:28px"><div class="grid g3">{"".join(guide_card(g, "") for g in GUIDES)}</div></div>'
    simple("guides.html", "Guides — Money, Business, Websites, AI & Number Culture", "In-depth guides on compound interest, break-even, margins, unit economics, website earnings, AI costs, domain investing and the culture of numbers.", body, "guides.html")

def build_videos():
    cats = sorted(set(v[3] for v in VIDEOS))
    body = hero_band("Video library", "Watch & learn", "Hand-picked lessons from respected educators on money, economics and AI. Videos load only when you press play, keeping the page fast and private.") + f'''<div class="wrap" style="padding-top:28px">
{"".join(f'<section style="padding:18px 0"><h2>{c}</h2><div class="grid g3">{"".join(video_card(v) for v in VIDEOS if v[3]==c)}</div></section>' for c in cats)}
<div class="card" style="margin-top:20px"><h3>Explore more on YouTube</h3><p>Curated search lists for deeper study:</p><p class="chips"><a class="chip" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query=break+even+analysis+explained">Break-even analysis</a><a class="chip" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query=unit+economics+cac+ltv">Unit economics</a><a class="chip" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query=how+mortgages+work">How mortgages work</a><a class="chip" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query=ai+for+small+business">AI for small business</a><a class="chip" target="_blank" rel="noopener" href="https://www.youtube.com/results?search_query=chinese+lucky+numbers+meaning">Chinese lucky numbers</a></p></div>
<div class="card" style="margin-top:16px"><h3>Are you a creator?</h3><p>Submit an educational video for our library or pitch a sponsored explainer.</p><p style="margin-top:10px"><a class="btn btn-teal" href="advertise.html#partner">Submit or partner</a></p></div>
<p class="muted" style="margin-top:16px;font-size:.85rem">Videos are embedded from YouTube and remain the property of their creators. {NAME} is not affiliated with these channels.</p></div>'''
    simple("videos.html", "Video Library — Money, Economics & AI Lessons", "Curated educational videos on compound interest, economics and artificial intelligence from leading creators.", body, "videos.html")

def build_plan():
    def opts(name, items):
        return '<div class="opts">' + "".join(f'<label class="opt"><input type="radio" name="{name}" value="{esc(i)}" required> {esc(i)}</label>' for i in items) + '</div>'
    body = hero_band("Free · personalised · no obligation", "Get your free growth & funding plan", "Five quick questions. A human-reviewed plan covering funding options, pricing, unit economics and the next three moves for your business or project.") + f'''<div class="wrap" style="padding-top:32px"><div class="grid plan-grid" style="align-items:start">
<div class="card funnel"><div class="progress" aria-hidden="true"><i id="pbar"></i></div>
<form data-form="Growth plan lead" id="planForm" data-ok="Done! Your request is in. Expect your personalised plan within 1–2 business days. Meanwhile, try our calculators.">{hp()}
<div class="step on" data-s="1"><h3>1. What do you want help with?</h3>{opts("goal",["Funding or a business loan","Grow revenue & fix pricing","Build a website, app or AI tool","Buy, sell or value a website/domain","Cut costs / extend runway","Personal finance & investing plan"])}</div>
<div class="step" data-s="2"><h3>2. Where are you today?</h3>{opts("stage",["Idea / pre-launch","Launched, under 1 year","Established 1–5 years","5+ years","Individual (not a business)"])}</div>
<div class="step" data-s="3"><h3>3. Monthly revenue (or income)</h3>{opts("revenue",["Under 5,000","5,000 – 25,000","25,000 – 100,000","100,000+","Prefer not to say"])}</div>
<div class="step" data-s="4"><h3>4. Budget & timeline</h3>
<div class="row"><div class="f"><label for="pb">Budget available</label><select id="pb" name="budget"><option>Not sure yet</option><option>Under 1,000</option><option>1,000 – 5,000</option><option>5,000 – 25,000</option><option>25,000+</option></select></div>
<div class="f"><label for="pt">Timeline</label><select id="pt" name="timeline"><option>As soon as possible</option><option>Within 1 month</option><option>1–3 months</option><option>Just exploring</option></select></div></div>
<div class="f"><label for="pn">Anything we should know? (optional)</label><textarea id="pn" name="details" rows="3" placeholder="e.g. we need 50k to buy inventory; margins are ~30%"></textarea></div></div>
<div class="step" data-s="5"><h3>5. Where should we send your plan?</h3>
<div class="row"><div class="f"><label for="nm">Full name</label><input id="nm" name="name" required autocomplete="name"></div><div class="f"><label for="em">Email</label><input id="em" type="email" name="email" required autocomplete="email"></div></div>
<div class="row"><div class="f"><label for="ph">Phone / WhatsApp (optional)</label><input id="ph" name="phone" type="tel" autocomplete="tel"></div><div class="f"><label for="co">Country</label><input id="co" name="country" autocomplete="country-name"></div></div>
<div class="f"><label for="bz">Business or website (optional)</label><input id="bz" name="business"></div>
{consent_box()}<label class="check"><input type="checkbox" name="partners" value="yes"> <span>Also match me with vetted funding or service partners (optional).</span></label></div>
<div class="steps-nav"><button type="button" class="btn btn-ghost" id="prevB" style="visibility:hidden">← Back</button><button type="button" class="btn btn-teal" id="nextB">Next →</button><button type="submit" class="btn btn-gold" id="subB" style="display:none">Send my free plan</button></div>
<p class="form-msg"></p></form>
<div class="trust"><span>🔒 Your data is never sold</span><span>⏱ 60 seconds</span><span>👤 Human-reviewed</span></div></div>
<div><div class="card"><h3>What's in your plan</h3><ul><li><b>Your numbers, decoded</b> — margin, break-even and runway checks.</li><li><b>Funding options</b> matched to your stage.</li><li><b>Pricing moves</b> that lift profit without losing customers.</li><li><b>Website & AI quick wins</b> to grow leads.</li><li><b>Three next steps</b> ranked by impact.</li></ul></div>
<div class="card" style="margin-top:16px"><h3>Prefer to talk?</h3><p>Use our <a href="contact.html">contact form</a> or <a href="#" data-mail="Growth plan question">email us</a>.</p></div>
<div class="card" style="margin-top:16px"><h3>Are you a lender, agency or advisor?</h3><p>Partner with us to receive qualified, opt-in leads.</p><p style="margin-top:8px"><a href="advertise.html#partner">Become a partner →</a></p></div></div>
</div></div>'''
    js = '''<script>(function(){var f=document.getElementById('planForm'),s=1,N=5,steps=f.querySelectorAll('.step'),bar=document.getElementById('pbar'),nx=document.getElementById('nextB'),pv=document.getElementById('prevB'),sb=document.getElementById('subB');
function show(){steps.forEach(function(x){x.classList.toggle('on',+x.dataset.s===s)});bar.style.width=(s/N*100)+'%';pv.style.visibility=s>1?'visible':'hidden';nx.style.display=s<N?'':'none';sb.style.display=s===N?'':'none'}
function valid(){var ok=true;f.querySelector('.step.on').querySelectorAll('input,select,textarea').forEach(function(i){if(!i.checkValidity()){ok=false}});if(!ok){var bad=f.querySelector('.step.on :invalid');bad&&bad.reportValidity&&bad.reportValidity()}return ok}
nx.addEventListener('click',function(){if(valid()){s++;show()}});pv.addEventListener('click',function(){s--;show()});
f.querySelectorAll('.step input[type=radio]').forEach(function(r){r.addEventListener('change',function(){if(s<N)setTimeout(function(){s++;show()},180)})});
f.addEventListener('submit',function(){setTimeout(function(){if(f.querySelector('.form-msg.ok')){s=1;show()}},1500)});show()})();</script>'''
    simple("get-a-plan.html", "Free Growth & Funding Plan — Personalised, No Obligation", "Answer five quick questions and get a free, human-reviewed plan for funding, pricing, unit economics, websites and AI growth.", body, "get-a-plan.html", scripts=js, body_attr=' data-nocta')

def build_support():
    tiers = [("5","Supporter","Covers hosting and a day of upkeep",""),("25","Builder","Funds a new calculator or guide update"," pop"),("100","Patron","Sponsors part of a monthly contest prize",""),("500","Founding Partner","Funds a hire sprint + name on our supporters wall","")]
    tier_html = "".join(f'<div class="card tier{p}"><h3>{n}</h3><div class="amt">${a}</div><p>{d}</p><p style="margin-top:12px"><button class="btn btn-gold btn-block" data-give="{a}">Give ${a}</button></p></div>' for a,n,d,p in tiers)
    alloc = [("Ongoing operations & hosting",30),("Marketing & promotions",25),("Hiring talent (writers, developers)",25),("Contests & prizes",20)]
    body = hero_band("Support " + NAME, "Keep the numbers free", "Every calculator, guide and contest here is free. Reader support funds operations, promotion, new talent and the monthly prize pool.") + f'''<div class="wrap" style="padding-top:32px">
<div class="grid g4">{tier_html}</div>
<div class="grid g2" style="margin-top:24px;align-items:start">
<div class="card"><h3>Give a custom amount</h3>
<div class="f"><label for="damt">Amount (USD)</label><input id="damt" type="number" min="1" step="1" value="50"></div>
<div class="f"><label for="dpur">Direct my support to</label><select id="dpur"><option>General operations</option><option>Marketing & promotions</option><option>Hiring talent</option><option>Contests & prizes</option></select></div>
<button class="btn btn-teal btn-block" id="dgo">Continue to secure checkout (PayPal)</button>
<p class="muted" style="font-size:.85rem;margin-top:8px">Payments are processed by PayPal; we never see your card details. Monthly giving can be selected at checkout. Contributions to {NAME} are not tax-deductible charitable donations.</p></div>
<div class="card"><h3>Where your support goes</h3><div class="alloc">{"".join(f'<div><div style="display:flex;justify-content:space-between;font-size:.92rem"><span>{n}</span><b>{p}%</b></div><div class="bar"><i style="width:{p}%"></i></div></div>' for n,p in alloc)}</div><p class="muted" style="margin-top:12px;font-size:.88rem">Target allocation; we publish an annual summary of how support was used.</p></div></div>
<div class="grid g2" style="margin-top:24px;align-items:start">
<div class="card"><h3>Sponsor a prize or pledge in-kind support</h3><p>Businesses can fund a contest prize, donate software licences or offer services to winners.</p>
<form data-form="Sponsorship pledge">{hp()}<div class="row"><div class="f"><label for="sp1">Name / company</label><input id="sp1" name="name" required></div><div class="f"><label for="sp2">Email</label><input id="sp2" type="email" name="email" required></div></div>
<div class="row"><div class="f"><label for="sp3">Pledge type</label><select id="sp3" name="pledge"><option>Cash prize</option><option>Product / software</option><option>Services for winners</option><option>Operations funding</option></select></div><div class="f"><label for="sp4">Approx. value (USD)</label><input id="sp4" name="value" type="number" min="0"></div></div>
<div class="f"><label for="sp5">Message</label><textarea id="sp5" name="message" rows="3"></textarea></div>{consent_box()}<button class="btn btn-teal" type="submit">Send pledge</button><p class="form-msg"></p></form></div>
<div class="card"><h3>Other ways to help (free)</h3><ul><li>Share a calculator link with someone it would help.</li><li>Suggest a calculator or report an error via our <a href="contact.html">contact form</a>.</li><li>Link to {NAME} from your blog or resource page.</li><li>Enter a <a href="contests.html">monthly contest</a>.</li><li>Join as a <a href="careers.html">contributor</a>.</li></ul>
<h3 style="margin-top:16px">Large gifts & partnerships</h3><p>For grants, naming rights or strategic partnerships, <a href="{INTEREST}" target="_blank" rel="noopener">contact us here</a>.</p></div></div></div>'''
    js = '''<script>document.querySelectorAll('[data-give]').forEach(function(b){b.addEventListener('click',function(){S67.donate(b.getAttribute('data-give'),document.getElementById('dpur').value)})});document.getElementById('dgo').addEventListener('click',function(){var a=document.getElementById('damt').value;if(!(a>0)){document.getElementById('damt').focus();return}S67.donate(a,document.getElementById('dpur').value)});</script>'''
    simple("support.html", "Support Us — Donate to Keep Free Calculators Free", "Support free calculators, guides and monthly contests. Choose a tier or custom amount, sponsor a prize or pledge in-kind support.", body, "support.html", scripts=js)

def build_contests():
    body = hero_band("Contests & prizes", "The 67858 Number Crunch", "A monthly challenge that rewards sharp thinking with numbers. Free to enter, open to students, founders and number nerds alike.") + f'''<div class="wrap" style="padding-top:32px">
<div class="grid g3"><div class="card"><div class="ico">🧩</div><h3>1. Solve</h3><p>Each month we post a real-world numbers puzzle — pricing, growth, probability or a number-pattern riddle.</p></div><div class="card"><div class="ico">📝</div><h3>2. Submit</h3><p>Send your answer and a short explanation (max 200 words) using the form below before the deadline.</p></div><div class="card"><div class="ico">🏆</div><h3>3. Win</h3><p>A panel scores accuracy, clarity and creativity. Winners are announced on this page and by email.</p></div></div>
<div class="grid g2" style="margin-top:24px;align-items:start">
<div class="card"><span class="tag">Current challenge</span><h3>The Rising Run</h3><p>A store sells one product at a price that climbs 6%, then 7%, then 8% over three successive months, and then is discounted 58% in a clearance sale. <b>Is the clearance price above or below 50% of the original price, and by how many percentage points?</b> Show your working.</p>
<p class="muted">Tip: our <a href="calculators/percentage-change-calculator.html">percentage change</a> and <a href="calculators/discount-calculator.html">discount</a> calculators help you check your logic.</p>
<h3 style="margin-top:16px">Prize pool</h3><ul><li>🥇 1st: $100 (or sponsor-provided equivalent)</li><li>🥈 2nd: $50</li><li>🥉 3rd: $25</li><li>⭐ Best explanation: featured on our site + a free growth plan</li></ul>
<p class="muted" style="font-size:.88rem">Prize amounts depend on sponsor and reader support; the final prize pool is confirmed on this page before judging. <a href="support.html">Fund the prize pool</a> or <a href="advertise.html">sponsor a contest</a>.</p></div>
<div class="card"><h3>Enter this month</h3><form data-form="Contest entry" data-ok="Entry received! Good luck — winners are announced after judging.">{hp()}
<div class="row"><div class="f"><label for="c1">Name</label><input id="c1" name="name" required></div><div class="f"><label for="c2">Email</label><input id="c2" type="email" name="email" required></div></div>
<div class="row"><div class="f"><label for="c3">Country</label><input id="c3" name="country" required></div><div class="f"><label for="c4">I am a…</label><select id="c4" name="category"><option>Student (18+)</option><option>Professional</option><option>Founder / business owner</option><option>Other</option></select></div></div>
<div class="f"><label for="c5">Your answer</label><input id="c5" name="answer" required></div>
<div class="f"><label for="c6">Your working (max 200 words)</label><textarea id="c6" name="working" rows="5" maxlength="1400" required></textarea></div>
<label class="check"><input type="checkbox" name="age" value="18+" required> <span>I am 18 or older (or the age of majority where I live) and accept the official rules below.</span></label>{consent_box("I agree that my name and country may be published if I win.")}
<button class="btn btn-gold btn-block" type="submit">Submit my entry</button><p class="form-msg"></p></form></div></div>
<section class="prose" style="padding:32px 0 0" id="rules"><h2>Official rules (summary)</h2><ol><li><b>No purchase or donation necessary</b> to enter or win. Donating does not improve your chances.</li><li>One entry per person per monthly challenge. Entries close at 23:59 UTC on the last day of the month.</li><li>Open to individuals 18+ (or the age of majority in their jurisdiction). Void where prohibited or restricted by law. Employees of {NAME} and its sponsors are not eligible.</li><li>This is a skill-based competition. Entries are judged on correctness (50%), clarity of explanation (30%) and creativity (20%). Judges' decisions are final.</li><li>Winners are notified by email and must respond within 14 days; otherwise an alternate winner may be selected. Prizes are paid via an electronic method agreed with the winner and are non-transferable. Winners are responsible for any taxes.</li><li>By entering, you grant {NAME} a non-exclusive licence to publish your explanation with credit.</li><li>We may modify or cancel a contest if circumstances beyond our control arise, and will post any change on this page.</li></ol>
<h2>Past winners</h2><p class="muted">The first season is underway — winners will be listed here after judging.</p></section></div>'''
    simple("contests.html", "Monthly Number Crunch Contest — Win Prizes", "Enter the free monthly 67858 Number Crunch challenge. Solve a real-world numbers puzzle, explain your logic and win sponsored prizes.", body, "contests.html")

def build_careers():
    roles = [("Finance & business writer","Remote · freelance","Write original, accurate guides with worked examples. Finance, accounting or economics background preferred."),
             ("Front-end / calculator developer","Remote · contract","Build fast, accessible calculators in vanilla JavaScript; write test cases for every formula."),
             ("Video creator / explainer","Remote · per project","Produce short explainers for YouTube and social that bring our calculators to life."),
             ("SEO & growth marketer","Remote · part-time","Own content strategy, internal linking, outreach and partnerships."),
             ("Community & contest moderator","Remote · part-time","Run monthly contests, judge entries and engage our community."),
             ("Campus & creator ambassadors","Remote · flexible","Share tools with your audience or campus and earn rewards.")]
    body = hero_band("Careers & talent", "Build the internet's friendliest numbers hub", "We hire remote, flexible talent worldwide. Show us your work — degrees matter less than accuracy and clarity.") + f'''<div class="wrap" style="padding-top:32px"><div class="grid g3">{"".join(f'<div class="card"><span class="tag">{l}</span><h3>{t}</h3><p>{d}</p></div>' for t,l,d in roles)}</div>
<div class="grid g2" style="margin-top:24px;align-items:start"><div class="card"><h3>Apply or join our talent pool</h3><form data-form="Careers application" data-ok="Application received — thank you! We review every application and reply if there's a fit.">{hp()}
<div class="row"><div class="f"><label for="a1">Name</label><input id="a1" name="name" required></div><div class="f"><label for="a2">Email</label><input id="a2" type="email" name="email" required></div></div>
<div class="row"><div class="f"><label for="a3">Role</label><select id="a3" name="role">{"".join(f"<option>{t}</option>" for t,_,_ in roles)}<option>Other / talent pool</option></select></div><div class="f"><label for="a4">Location / time zone</label><input id="a4" name="location"></div></div>
<div class="f"><label for="a5">Portfolio, LinkedIn or GitHub link</label><input id="a5" name="portfolio" type="url" placeholder="https://"></div>
<div class="f"><label for="a6">Why you, in 3 sentences</label><textarea id="a6" name="pitch" rows="4" required></textarea></div>
<div class="row"><div class="f"><label for="a7">Availability</label><select id="a7" name="availability"><option>Under 10 h/week</option><option>10–20 h/week</option><option>20+ h/week</option></select></div><div class="f"><label for="a8">Expected rate (USD/h)</label><input id="a8" name="rate" type="number" min="0"></div></div>
{consent_box()}<button class="btn btn-teal" type="submit">Submit application</button><p class="form-msg"></p></form></div>
<div class="card"><h3>How we work</h3><ul><li>Fully remote, async-first.</li><li>Paid per project or hourly; rates agreed up front.</li><li>Every formula is tested; every guide is fact-checked.</li><li>Contributors get bylines and portfolio-ready work.</li></ul><h3 style="margin-top:14px">Hiring for your business?</h3><p>Partner with us to reach finance-literate talent — <a href="advertise.html">see sponsorship options</a>.</p></div></div></div>'''
    simple("careers.html", "Careers — Writers, Developers, Creators & Ambassadors", "Join 67858.com remotely: finance writers, calculator developers, video creators, growth marketers, moderators and ambassadors.", body, "", )

def build_advertise():
    pk = [("Calculator sponsor","Your brand on a calculator page: logo, short message and link next to results (clearly labelled as sponsored)."),
          ("Contest sponsor","Fund a monthly prize and get naming credit, entrant reach and a winner announcement feature."),
          ("Newsletter sponsor","A labelled placement in the weekly Numbers Brief."),
          ("Lead partner","Receive opt-in leads from our free growth plan in your category (funding, web, accounting, AI)."),
          ("Sponsored guide or video","An expert explainer produced to our editorial standards, labelled as sponsored."),
          ("Widget licensing","Embed our calculators on your website under your brand.")]
    body = hero_band("Advertise · sponsor · partner", "Reach people making money decisions", "Founders, freelancers, homebuyers and investors use our tools at the exact moment they are deciding. Put your brand there — transparently labelled.") + f'''<div class="wrap" style="padding-top:32px"><div class="grid g3">{"".join(f'<div class="card"><div class="ico">📣</div><h3>{t}</h3><p>{d}</p></div>' for t,d in pk)}</div>
<div class="grid g2" style="margin-top:24px;align-items:start" id="partner"><div class="card"><h3>Request a media kit or partnership</h3><form data-form="Advertising / partnership inquiry" data-ok="Thanks! We'll send our media kit and options within 1–2 business days.">{hp()}
<div class="row"><div class="f"><label for="ad1">Name</label><input id="ad1" name="name" required></div><div class="f"><label for="ad2">Work email</label><input id="ad2" type="email" name="email" required></div></div>
<div class="row"><div class="f"><label for="ad3">Company</label><input id="ad3" name="company" required></div><div class="f"><label for="ad4">Website</label><input id="ad4" name="website" type="url" placeholder="https://"></div></div>
<div class="row"><div class="f"><label for="ad5">Interested in</label><select id="ad5" name="interest">{"".join(f"<option>{t}</option>" for t,_ in pk)}<option>Buying the domain / website</option></select></div><div class="f"><label for="ad6">Monthly budget (USD)</label><select id="ad6" name="budget"><option>Under 500</option><option>500 – 2,000</option><option>2,000 – 10,000</option><option>10,000+</option></select></div></div>
<div class="f"><label for="ad7">Goals</label><textarea id="ad7" name="message" rows="4"></textarea></div>{consent_box()}<button class="btn btn-teal" type="submit">Request media kit</button><p class="form-msg"></p></form></div>
<div class="card"><h3>Interested in this domain or website?</h3><p>{NAME} — the website, brand and domain — is open to acquisition, investment, sponsorship and strategic partnership offers.</p><p style="margin-top:10px"><a class="btn btn-gold btn-block" href="{INTEREST}" target="_blank" rel="noopener">Contact about domain / partnership</a></p>
<h3 style="margin-top:18px">Our standards</h3><ul><li>All paid placements are clearly labelled.</li><li>Sponsors never influence calculator results or editorial conclusions.</li><li>We do not accept ads for predatory lending, gambling or misleading offers.</li><li>Sponsored content is kept separate from Google ad units.</li></ul></div></div></div>'''
    simple("advertise.html", "Advertise, Sponsor & Partner", "Sponsor calculators, contests and newsletters, receive opt-in leads or license our widgets. Transparent, labelled placements.", body, "")

def build_contact():
    body = hero_band("Contact", "Talk to the 67858 team", "Questions, corrections, partnership ideas or calculator suggestions — we read every message.") + f'''<div class="wrap" style="padding-top:32px"><div class="grid g2" style="align-items:start"><div class="card"><h3>Send us a message</h3><form data-form="Contact form">{hp()}
<div class="row"><div class="f"><label for="k1">Name</label><input id="k1" name="name" required></div><div class="f"><label for="k2">Email</label><input id="k2" type="email" name="email" required></div></div>
<div class="f"><label for="k3">Topic</label><select id="k3" name="topic"><option>General question</option><option>Report an error / correction</option><option>Suggest a calculator</option><option>Advertising / sponsorship</option><option>Domain / website acquisition</option><option>Partnership</option><option>Press</option><option>Privacy request</option></select></div>
<div class="f"><label for="k4">Message</label><textarea id="k4" name="message" rows="6" required></textarea></div>{consent_box()}<button class="btn btn-teal" type="submit">Send message</button><p class="form-msg"></p></form></div>
<div class="grid" style="gap:16px"><div class="card"><h3>Email</h3><p>Prefer your own email app? <a href="#" data-mail="Inquiry from 67858.com">Click here to email us</a>.</p></div>
<div class="card"><h3>Domain, sponsorship, advertising & partnerships</h3><p>Interested in this website or domain name, sponsorship, advertising or partnership?</p><p style="margin-top:10px"><a class="btn btn-gold" href="{INTEREST}" target="_blank" rel="noopener">Contact via web.works</a></p></div>
<div class="card"><h3>Response time</h3><p>We aim to reply within 1–2 business days. For corrections, please include the page URL and the inputs you used.</p></div></div></div></div>'''
    simple("contact.html", "Contact Us", "Contact 67858.com for questions, corrections, calculator suggestions, advertising, sponsorship, domain acquisition and partnerships.", body, "")

def legal(path, title, desc, content):
    body = hero_band("Legal & policies" if path!="about.html" else "About", title, desc) + f'<div class="wrap" style="padding-top:28px"><article class="prose">{content}<p class="muted">Last updated: {UPDATED}</p></article></div>'
    simple(path, title, desc, body, "")

def build_legal():
    legal("about.html", "About 67858.com", "Free tools and honest explanations that help people make better decisions with numbers.", f'''
<h2>Our mission</h2><p>{NAME} exists to make the numbers behind everyday money decisions instant and understandable. Whether you are pricing a product, comparing loans, valuing a website or budgeting for AI tools, you should be able to see the answer — and the formula behind it — in seconds, for free.</p>
<h2>What we publish</h2><ul><li><b>{len(CALCS)} calculators</b> across money, business, websites & AI and everyday maths, each with its formula, a worked example and FAQs.</li><li><b>The Number Lab</b>, which analyses any number's mathematics, cultural symbolism and memorability.</li><li><b>In-depth guides</b> written in plain English with numbers you can verify.</li><li><b>A curated video library</b> from respected educators.</li><li><b>Monthly contests</b> that reward clear thinking with numbers.</li></ul>
<h2>Why “67858”?</h2><p>Our name is our domain. Read aloud it is “678-58”: a rising sequence — six, seven, eight — followed by fifty-eight, which in Chinese number culture is often read as “I prosper”. We liked the idea of a name that encodes steady upward progress. It also starts with “67”, the number-meme that became a 2025 Word of the Year — a reminder that numbers can be fun.</p>
<h2>How we stay accurate</h2><p>Every calculator formula is tested against hand-worked examples before publication. See our <a href="editorial-policy.html">editorial policy</a> for methodology, corrections and independence standards.</p>
<h2>How we are funded</h2><p>The site is free to use. It is supported by advertising (including Google AdSense), clearly labelled sponsorships, partner referrals from our opt-in growth-plan form, and <a href="support.html">reader support</a>. Advertisers never influence calculator results.</p>
<h2>Contact</h2><p>Reach us through our <a href="contact.html">contact page</a>. For domain, sponsorship, advertising or partnership interest, <a href="{INTEREST}" target="_blank" rel="noopener">contact us via web.works</a>.</p>''')
    legal("editorial-policy.html", "Editorial Policy & Methodology", "How we build, test, review and correct our calculators and guides.", f'''
<h2>Accuracy first</h2><p>Each calculator implements a standard, published formula shown on its page. Before publishing we verify outputs against independently hand-calculated examples, and each worked example on a calculator page is generated from the same code that powers the tool.</p>
<h2>Sources</h2><p>We rely on standard financial mathematics, official statistics and reputable reference works. Cultural content (such as number symbolism) is presented as tradition and belief, never as prediction. Where we summarise reporting, we paraphrase and credit the original publisher.</p>
<h2>Review & updates</h2><p>Pages display the date they were last reviewed. We revisit calculators when underlying rules or common assumptions change.</p>
<h2>Independence</h2><p>Advertisers, sponsors and partners have no influence over calculator logic, results or editorial conclusions. Sponsored content is always labelled.</p>
<h2>Corrections</h2><p>Found an error? Use our <a href="contact.html">contact form</a> with the page URL and inputs. Verified corrections are fixed promptly and noted where material.</p>
<h2>Not advice</h2><p>Our content is educational. It is not personalised financial, investment, tax or legal advice. Consult a qualified professional for decisions about your situation.</p>''')
    legal("privacy.html", "Privacy Policy", "What we collect, why, and the choices you have — including cookies and Google advertising.", f'''
<h2>Summary</h2><p>Calculators run entirely in your browser; the numbers you type are not sent to us. We only receive information you choose to submit through a form (for example your name and email), plus standard technical data needed to serve and advertise on the site.</p>
<h2>Information we collect</h2><ul><li><b>Form submissions:</b> name, email and the details you provide in contact, growth-plan, contest, career, sponsorship or newsletter forms. Forms are delivered to our inbox via a form-processing service (FormSubmit).</li><li><b>Local storage:</b> preferences such as theme, currency symbol, cookie choice and recent calculations are stored only on your device.</li><li><b>Technical data:</b> our host (GitHub Pages) and advertising partners may process IP address, browser type and pages viewed for security and delivery.</li></ul>
<h2>Advertising and cookies</h2><p>We use Google AdSense to display ads. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads based on visits to this site and/or other sites on the Internet. You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a> or <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">www.aboutads.info</a>. Learn how Google uses data at <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">How Google uses information from sites or apps that use its services</a>.</p>
<p>Visitors in the EEA, UK and Switzerland are shown a Google-certified consent message before personalised ads are served. You can change your choice at any time by clearing this site's cookies.</p>
<h2>Donations</h2><p>Donations are processed by PayPal under PayPal's privacy policy. We receive the payer's name, email and amount, never card details.</p>
<h2>How we use information</h2><ul><li>To respond to your request and deliver your growth plan.</li><li>To run contests and contact winners.</li><li>To send the newsletter if you subscribed (unsubscribe anytime).</li><li>If you opt in, to introduce you to relevant partners — we never sell your data.</li></ul>
<h2>Retention & rights</h2><p>We keep submissions only as long as needed for the purpose. Depending on where you live (for example under GDPR, UK GDPR, CCPA/CPRA, PIPEDA or Québec's Law 25), you may request access, correction, deletion or portability of your data, or withdraw consent. Use our <a href="contact.html">contact form</a> and choose “Privacy request”.</p>
<h2>Children</h2><p>This site is not directed to children under 13, and contests are open only to adults.</p>
<h2>Changes</h2><p>We will post any changes to this policy on this page with a new date.</p>''')
    legal("terms.html", "Terms of Use", "The rules for using 67858.com, its calculators, content and contests.", f'''
<h2>Acceptance</h2><p>By using {NAME} you agree to these terms. If you do not agree, please do not use the site.</p>
<h2>Educational use</h2><p>Calculators, guides and the Number Lab provide estimates and general information only. They are not financial, investment, tax, legal or professional advice, and results may not reflect your circumstances. You are responsible for decisions you make.</p>
<h2>Intellectual property</h2><p>Original text, code, design and calculators on this site are owned by {NAME} and protected by copyright. You may share links and quote brief excerpts with attribution. Embedded videos and third-party marks belong to their respective owners.</p>
<h2>Acceptable use</h2><p>Do not attempt to disrupt the site, scrape it at scale, submit spam through forms, or misuse contest systems.</p>
<h2>User submissions</h2><p>By submitting content (for example contest entries) you confirm it is your own and grant us a non-exclusive licence to use it as described on the relevant page.</p>
<h2>Third-party links & services</h2><p>We link to and use third-party services (YouTube, PayPal, Google, FormSubmit, web.works). We are not responsible for their content or practices.</p>
<h2>Disclaimer of warranties & limitation of liability</h2><p>The site is provided “as is” without warranties of any kind. To the maximum extent permitted by law, {NAME} is not liable for any loss arising from use of the site or reliance on its content.</p>
<h2>Changes</h2><p>We may update these terms; continued use means acceptance of the updated terms.</p>''')
    legal("disclaimer.html", "Disclaimer", "Important limits on the calculators, guides, number symbolism and partner referrals.", f'''
<h2>Not professional advice</h2><p>All content on {NAME} is for general educational purposes. Nothing here is a recommendation to buy, sell or borrow, or a substitute for advice from a licensed professional.</p>
<h2>Estimates only</h2><p>Calculator outputs depend on your inputs and simplifying assumptions. Actual loan terms, taxes, returns, fees and prices will differ.</p>
<h2>Number symbolism & numerology</h2><p>The Number Lab's cultural meanings and numerology are presented as traditions and for entertainment. They do not predict outcomes and should not guide financial decisions.</p>
<h2>Advertising, sponsorship & referrals</h2><p>We display Google ads and labelled sponsorships, and may receive compensation when you opt in to be introduced to a partner. This never changes calculator results.</p>
<h2>External content</h2><p>Videos and links to third-party sites are provided for convenience; their owners are responsible for their accuracy.</p>''')
    legal("trademark.html", "Trademark & Copyright Disclosure", "How 67858.com uses the number 67858 and respects third-party rights.", f'''
<h2>Use of “67858”</h2><p>“67858” is used on this website solely as the identifier of our domain name, <b>67858.com</b>. A number string of this kind is descriptive and generic; we do not claim exclusive rights to the number itself, and we do not use it to suggest any connection with a third party.</p>
<h2>No affiliation</h2><p>{NAME} is independent. It is not affiliated with, endorsed by or sponsored by any company, product, part number, postal code, telephone number, government body, artist, athlete, publisher or platform that uses or is associated with “67858”, “678”, “58”, “67” or “6-7”. References to third parties — including Dictionary.com, YouTube channels, Google, PayPal and others — are factual and editorial (nominative) and do not imply endorsement.</p>
<h2>Third-party trademarks</h2><p>All third-party names, logos and trademarks are the property of their respective owners and are used only to identify those owners or their services.</p>
<h2>Copyright</h2><p>© {datetime.date.today().year} {NAME}. Original site text, calculators, code, graphics and layout are protected by copyright. Embedded YouTube videos remain the property of their creators and are shown via YouTube's standard embed player. Summaries of third-party reporting are paraphrased and credited.</p>
<h2>Infringement notices</h2><p>If you believe content on this site infringes your rights, please send a notice through our <a href="contact.html">contact form</a> (topic: “Report an error / correction”) identifying the material, your rights and your contact details. We review notices promptly and remove infringing material where appropriate.</p>
<h2>Domain & brand inquiries</h2><p>For inquiries about the domain, website, sponsorship, advertising or partnership, <a href="{INTEREST}" target="_blank" rel="noopener">contact us via web.works</a>.</p>''')

def build_glossary():
    terms = [("APR","Annual percentage rate: the yearly cost of borrowing, which may include certain fees."),("Amortization","Paying off a loan through scheduled payments that cover interest first, then principal."),("Break-even point","Sales volume where revenue equals total costs."),("CAC","Customer acquisition cost: sales and marketing spend ÷ new customers."),("CAGR","Compound annual growth rate: the steady yearly rate that turns a start value into an end value."),("Churn","The share of customers lost in a period."),("Contribution margin","Price minus variable cost per unit; what each sale contributes to fixed costs."),("CPM","Cost per thousand ad impressions, paid by advertisers."),("CTR","Click-through rate: clicks ÷ impressions."),("DTI","Debt-to-income ratio: monthly debt payments ÷ gross monthly income."),("EMI","Equated monthly instalment: a fixed loan payment covering interest and principal."),("Gross margin","(Revenue − direct costs) ÷ revenue."),("Inflation","The rate at which prices rise and purchasing power falls."),("LTV","Customer lifetime value: gross profit expected from a customer over the relationship."),("Markup","Profit ÷ cost."),("Net burn","Monthly expenses minus revenue — the cash a company loses each month."),("Page RPM","Ad revenue per 1,000 pageviews."),("Principal","The original amount borrowed or invested."),("ROI","Return on investment: (gain − cost) ÷ cost."),("Rule of 72","72 ÷ annual rate ≈ years to double money."),("Runway","Months until cash runs out at the current burn."),("Token","A unit of text processed by an AI model; roughly ¾ of an English word on average."),("Digital root","The single digit obtained by repeatedly summing a number's digits.")]
    body = hero_band("Glossary", "Money & numbers glossary", "Short, precise definitions for the terms used across our calculators and guides.") + '<div class="wrap" style="padding-top:28px"><div class="prose"><dl>' + "".join(f'<dt id="{t.lower().replace(" ","-")}"><b>{t}</b></dt><dd style="margin:0 0 14px">{d}</dd>' for t,d in terms) + '</dl></div></div>'
    schema=[{"@context":"https://schema.org","@type":"DefinedTermSet","name":"67858.com glossary","hasDefinedTerm":[{"@type":"DefinedTerm","name":t,"description":d} for t,d in terms]}]
    simple("glossary.html", "Glossary — Finance, Business & Number Terms", "Plain definitions of APR, EMI, CAC, LTV, churn, RPM, CAGR, runway, tokens and more.", body, "", schema=schema)

def build_misc():
    write("404.html", page("404.html", "Page not found", "This page could not be found.", hero_band("404", "That number doesn't add up", "The page you're looking for isn't here. Try a calculator or the Number Lab.", '<p><a class="btn btn-gold" href="/">Home</a> <a class="btn btn-ghost" style="color:#fff!important" href="/calculators.html">Calculators</a></p>'), "", r="/"))
    write("_layouts/default.html", layout_html())
    for n,h in INCLUDES.items(): write("_includes/"+n, h)
    write("_config.yml", "title: 67858.com\nmarkdown: kramdown\nexclude: [src, README.md, PROMPTS.md, \"*.py\"]\ninclude: [ads.txt]\n")
    write("CNAME", "67858.com\n")
    urls = ["", "calculators.html","number-lab.html","guides.html","videos.html","get-a-plan.html","support.html","contests.html","careers.html","advertise.html","contact.html","about.html","editorial-policy.html","glossary.html","privacy.html","terms.html","disclaimer.html","trademark.html"] + [f"calculators/{c['slug']}.html" for c in CALCS] + [f"guides/{g['slug']}.html" for g in GUIDES]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f'  <url><loc>{SITE}{u}</loc><lastmod>{ISO}</lastmod><changefreq>{"weekly" if u in ("","calculators.html","guides.html","contests.html") else "monthly"}</changefreq><priority>{"1.0" if u=="" else "0.8" if u.startswith(("calculators","guides","number")) else "0.5"}</priority></url>\n' for u in urls) + '</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
    write("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    write("site.webmanifest", json.dumps({"name":f"{NAME} — {TAG}","short_name":"67858","start_url":"./index.html","display":"standalone","background_color":"#0d1321","theme_color":"#0d1321","icons":[{"src":"assets/img/favicon.svg","sizes":"any","type":"image/svg+xml"}]}, indent=2))
    write("assets/img/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0d1321"/><text x="32" y="29" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="19" text-anchor="middle" fill="#e8a317">678</text><text x="32" y="50" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="19" text-anchor="middle" fill="#3fd1bc">58</text></svg>')
    with open(os.path.join(os.path.dirname(__file__), "main.js"), encoding="utf-8") as f:
        write("assets/js/main.js", f.read().replace("__EMAILCODES__", email_codes()))

if __name__ == "__main__":
    for c in CALCS: build_calc(c)
    for g in GUIDES: build_guide(g)
    build_home(); build_hub(); build_lab(); build_guides_hub(); build_videos(); build_plan(); build_support(); build_contests(); build_careers(); build_advertise(); build_contact(); build_legal(); build_glossary(); build_misc()
    print(f"Built {len(CALCS)} calculators, {len(GUIDES)} guides and core pages.")
