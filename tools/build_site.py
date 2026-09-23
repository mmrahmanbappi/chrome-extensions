#!/usr/bin/env python3
"""Builds the GitHub Pages website for the SEO Chrome extensions.

Run from the repository root:  python3 tools/build_site.py

It reads each extension's README.md and manifest.json in technical-seo/,
and writes index.html, one page per tool, 404.html, sitemap.xml and
robots.txt. Images live in images/ (see tools/make_images.py).
"""
import html
import json
import os
import re
from datetime import date

import markdown

BASE = "https://mmrahmanbappi.github.io/chrome-extensions"
REPO = "https://github.com/mmrahmanbappi/chrome-extensions"
DL = REPO + "/releases/latest/download"
AUTHOR = {
    "@type": "Person",
    "@id": BASE + "/#author",
    "name": "MM Rahman Bappi",
    "url": "https://mmseo.app/",
    "jobTitle": "Technical SEO consultant and web developer",
    "sameAs": ["https://github.com/mmrahmanbappi", "https://mmseo.app/"],
}
TODAY = date.today().isoformat()

# Extra copy for each tool: card line, search phrase, and one tool-specific FAQ.
EXTRA = {
    "orphan-page-finder": dict(
        card="Finds pages in your sitemap that no internal link points to.",
        phrase="Find orphan pages in your sitemap",
        q="How many pages can it scan?",
        a="Up to 5,000 pages in one scan. Progress is saved, so you can close the browser and continue later."),
    "click-depth-mapper": dict(
        card="Shows how many clicks each page is from your homepage.",
        phrase="Check the click depth of every page",
        q="What is a good click depth?",
        a="Important pages should be three clicks or fewer from the homepage. Deeper pages are found and crawled less often, so link to them from pages that are closer to the top."),
    "canonical-chain-tracer": dict(
        card="Follows canonical tags and finds chains and loops.",
        phrase="Find canonical chains and loops",
        q="What is a canonical chain?",
        a="A chain is when page A says page B is the real version, but page B points to page C. A loop is when the chain comes back to where it started. Both make it harder for search engines to pick the right page."),
    "crawl-budget-waste-finder": dict(
        card="Finds filter, tracking and session URLs that waste crawl budget.",
        phrase="Find URLs that waste your crawl budget",
        q="How do I fix the URLs it finds?",
        a="For each URL it shows whether it is already handled by a canonical tag, a noindex tag or a robots.txt rule. The ones marked as open are the ones to fix first."),
    "two-mb-crawl-limit-monitor": dict(
        card="Finds pages close to or over Googlebot's 2MB crawl limit.",
        phrase="Check pages against Google's 2MB crawl limit",
        q="Does the 2MB limit include images and scripts?",
        a="No. The limit is about the HTML file itself, the bytes Googlebot downloads for the page. This tool measures exactly that, not the full weight a browser loads."),
    "full-site-cache-auditor": dict(
        card="Runs 54 checks on caching, CDN and DNS.",
        phrase="Audit caching, CDN and DNS in one scan",
        q="Do I need access to my server or CDN account?",
        a="No. It reads the public responses your site sends, the same way a visitor's browser or a crawler would."),
    "full-site-security-auditor": dict(
        card="Runs 47 security, DNS and CMS checks.",
        phrase="Run a full website security check",
        q="Does it attack or test my site in a risky way?",
        a="No. Nothing is actively exploited. It only looks at what is publicly visible and flags things for you to review."),
}
ORDER = ["orphan-page-finder", "click-depth-mapper", "canonical-chain-tracer", "crawl-budget-waste-finder",
         "two-mb-crawl-limit-monitor", "full-site-cache-auditor", "full-site-security-auditor"]

PERMS = {
    "storage": "Save your settings and scan results in your browser.",
    "unlimitedStorage": "Store results for large sites with thousands of pages.",
    "downloads": "Save Excel and PDF reports to your computer.",
    "tabs": "Read the address of the tab you have open, so it knows which site to scan.",
    "scripting": "Read links on pages that need JavaScript to show them.",
}


def md(text):
    return markdown.markdown(text.strip(), extensions=["sane_lists"])


def esc(s):
    return html.escape(s, quote=True)


def parse_readme(path):
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"^## ", text, flags=re.M)
    head, sections = parts[0], {}
    for p in parts[1:]:
        title, _, body = p.partition("\n")
        sections[title.strip()] = body.strip()
    intro = [l for l in head.split("\n") if l.strip() and not l.startswith(("#", "![", "Full guide"))]
    return " ".join(intro).strip(), sections


def load_tools():
    tools = []
    for slug in ORDER:
        d = f"technical-seo/{slug}"
        m = json.load(open(f"{d}/manifest.json"))
        intro, sec = parse_readme(f"{d}/README.md")
        does_key = next((k for k in sec if k.startswith("What it")), None)
        limits_key = next((k for k in sec if k in ("Good to know", "One thing this cannot see", "Limits")), None)
        features = re.findall(r"^- (.+)$", sec.get(does_key, ""), flags=re.M)
        tools.append(dict(slug=slug, name=m["name"], version=m["version"], desc=m["description"],
                          perms=m.get("permissions", []), intro=intro, sec=sec, does_key=does_key,
                          limits_key=limits_key, features=features, **EXTRA[slug]))
    return tools


CSS = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#15251d;--text:#28332d;--muted:#5d6862;--line:#e3e1d9;--green:#16835a;--green-soft:#e3f2ea;--max:70rem}
@media (prefers-color-scheme:dark){:root{--bg:#121714;--card:#1a211d;--ink:#eef3ef;--text:#dce4df;--muted:#9eaaa3;--line:#2a332e;--green:#5fcf9c;--green-soft:#1d3228}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:1.08rem/1.7 system-ui,-apple-system,"Segoe UI",Roboto,Ubuntu,sans-serif}
a{color:var(--green);text-underline-offset:3px}
:focus-visible{outline:3px solid var(--green);outline-offset:3px;border-radius:3px}
img{max-width:100%;height:auto;display:block}
.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:var(--ink);color:var(--bg);padding:.5rem 1rem;z-index:9}
.wrap{max-width:var(--max);margin:0 auto;padding-left:1.25rem;padding-right:1.25rem}
.narrow{max-width:46rem}
header.top{border-bottom:1px solid var(--line);background:var(--bg)}
header.top .wrap{display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;min-height:4rem}
.brand{font-weight:800;color:var(--ink);text-decoration:none;font-size:1.1rem;letter-spacing:-.01em}
header nav{display:flex;gap:1.3rem;flex-wrap:wrap;font-size:1rem}
header nav a{color:var(--text);text-decoration:none}header nav a:hover{color:var(--green)}
h1,h2,h3{color:var(--ink);line-height:1.2;letter-spacing:-.015em}
h1{font-size:clamp(2.1rem,5vw,3.2rem);margin:.2rem 0 1rem}
h2{font-size:clamp(1.5rem,3vw,1.95rem);margin:0 0 1rem}
h3{font-size:1.2rem;margin:0 0 .4rem}
p{margin:0 0 1.1rem}
.crumbs{font-size:.95rem;color:var(--muted);padding-top:1.4rem}
.crumbs a{color:var(--muted)}
.hero{padding:2.2rem 0 2.5rem}
.hero-grid{display:grid;grid-template-columns:1fr 1.15fr;gap:3rem;align-items:center}
.hero .icon{width:64px;height:64px;border-radius:14px}
.phrase{font-size:1.25rem;color:var(--muted);margin-bottom:1.2rem}
.lead{font-size:1.2rem}
.actions{display:flex;gap:.8rem;flex-wrap:wrap;margin:1.6rem 0 .8rem}
.btn{display:inline-block;padding:.85rem 1.4rem;border-radius:10px;font-weight:700;text-decoration:none;border:2px solid var(--green)}
.btn.main{background:var(--green);color:#fff}.btn.main:hover{filter:brightness(1.08)}
@media (prefers-color-scheme:dark){.btn.main{color:#0d1a13}}
.btn.alt{color:var(--green)}.btn.alt:hover{background:var(--green-soft)}
.small{font-size:.95rem;color:var(--muted)}
figure{margin:0}
figure img{border-radius:14px;border:1px solid var(--line);background:var(--card)}
figcaption{font-size:.93rem;color:var(--muted);margin-top:.6rem}
section.band{padding:3.2rem 0;border-top:1px solid var(--line)}
section.band.alt{background:var(--card)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem}
ul.checks{list-style:none;padding:0;margin:0;columns:2 20rem;column-gap:2.5rem}
ul.checks li{break-inside:avoid;padding:.45rem 0 .45rem 1.8rem;position:relative}
ul.checks li::before{content:"";position:absolute;left:0;top:.95rem;width:.8rem;height:.45rem;border-left:3px solid var(--green);border-bottom:3px solid var(--green);transform:rotate(-45deg)}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:0;display:grid;gap:1rem}
ol.steps li{counter-increment:s;position:relative;padding:1rem 1.2rem 1rem 3.8rem;background:var(--card);border:1px solid var(--line);border-radius:12px}
section.band.alt ol.steps li{background:var(--bg)}
ol.steps li::before{content:counter(s);position:absolute;left:1.1rem;top:.9rem;width:1.9rem;height:1.9rem;border-radius:50%;background:var(--green);color:#fff;font-weight:700;display:grid;place-items:center;font-size:.95rem}
@media (prefers-color-scheme:dark){ol.steps li::before{color:#0d1a13}}
code{font-family:ui-monospace,"Cascadia Code",Menlo,Consolas,monospace;font-size:.92em;background:var(--green-soft);padding:.1em .35em;border-radius:5px}
table.perm{width:100%;border-collapse:collapse}
table.perm th,table.perm td{text-align:left;padding:.7rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
table.perm th{width:11rem;color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(19rem,1fr));gap:1.2rem;list-style:none;padding:0;margin:0}
.grid a.card{display:flex;gap:1rem;align-items:flex-start;padding:1.2rem;background:var(--card);border:1px solid var(--line);border-radius:14px;text-decoration:none;color:inherit;height:100%}
section.band.alt .grid a.card{background:var(--bg)}
.grid a.card:hover{border-color:var(--green)}
.grid img{width:48px;height:48px;border-radius:10px;flex:none}
.grid h3{font-size:1.1rem;margin:0 0 .25rem}
.grid p{margin:0;color:var(--muted);font-size:.98rem}
details{border-bottom:1px solid var(--line);padding:1rem 0}
summary{font-weight:700;color:var(--ink);cursor:pointer;font-size:1.08rem}
details p{margin:.7rem 0 0}
.note{border-left:4px solid var(--green);background:var(--green-soft);padding:1rem 1.2rem;border-radius:0 10px 10px 0}
footer{border-top:1px solid var(--line);padding:2rem 0;color:var(--muted);font-size:.95rem}
footer .wrap{display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}
footer p{margin:0}
@media (max-width:860px){.hero-grid,.two{grid-template-columns:1fr;gap:2rem}}

/* Shared look with mmrahmanbappi.github.io */
:root{--bg:#eeeeea;--card:#fff;--ink:#171518;--text:#403b42;--muted:#5f5d61;--line:#d9d8d2;--green:#b23a0a;--green-soft:#f6e3d9;--max:78rem;--mt-accink:#fff;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--bg:#141316;--card:#222126;--ink:#f2f1ed;--text:#d7d5d9;--muted:#a3a1a6;--line:#302f35;--green:#ff7b4f;--green-soft:#3a2219;--mt-accink:#141316;color-scheme:dark}}
body{font-family:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:1.03rem;line-height:1.65}
a{color:var(--ink)}
h1,h2,h3{letter-spacing:-.035em;line-height:1.05}h1{font-weight:560}h2,h3{font-weight:600}
header.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:.6rem;font-weight:700;color:var(--ink);text-decoration:none;letter-spacing:-.01em}
.brand i{width:2.1rem;height:2.1rem;border-radius:50%;background:var(--ink);color:var(--bg);display:grid;place-items:center;font-style:normal;font-size:.7rem;font-weight:800;flex:none}
header.top nav{align-items:center}header.top nav a{color:var(--muted);text-decoration:none}header.top nav a:hover{color:var(--ink)}
header.top nav a.gh{border:1.5px solid var(--ink);border-radius:999px;padding:.35rem 1rem;color:var(--ink);font-weight:600}
.btn{border-radius:999px!important;font-weight:600}.btn.main{background:var(--ink)!important;border-color:var(--ink)!important;color:var(--bg)!important}
.card{border-radius:18px}
ol.steps li::before{color:var(--mt-accink)}
@media (max-width:760px){header.top nav a:not(.gh){display:none}}
"""


def page(title, desc, path, og, schema, body):
    url = BASE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="MM Rahman Bappi">
<meta name="theme-color" content="#16835a">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Free SEO Chrome Extensions">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/images/og/{og}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(title)}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}/images/og/{og}.jpg">
<link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{BASE}/site.css">
<script type="application/ld+json">
{json.dumps(schema, indent=1, ensure_ascii=False)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="{BASE}/"><i aria-hidden="true">SEO</i>Free SEO Chrome Extensions</a>
<nav aria-label="Main"><a href="{BASE}/#tools">All tools</a><a href="{BASE}/#install">How to install</a><a href="{BASE}/#faq">FAQ</a><a href="https://mmrahmanbappi.github.io/">All projects</a><a class="gh" href="{REPO}">GitHub</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
<p>Made by <a href="https://mmseo.app/">MM Rahman Bappi</a>, technical SEO consultant and web developer.</p>
<p>Free and open source under the MIT license. <a href="{REPO}">Source on GitHub</a> &nbsp; <a href="https://mmrahmanbappi.github.io/">More free projects</a></p>
</div></footer>
</body>
</html>
"""


def website_node():
    return {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Free SEO Chrome Extensions",
            "description": "Seven free Chrome extensions for technical SEO audits.", "inLanguage": "en",
            "publisher": {"@id": BASE + "/#author"}}


def install_steps(zipname, folder):
    got = (f"You will get a folder called <code>{esc(folder)}</code>." if folder
           else "You will get one folder for each tool. Install the ones you want.")
    return f"""<ol class="steps">
<li><strong>Download the zip file</strong> with the button on this page and unzip it. {got}</li>
<li><strong>Open the extensions page.</strong> In Chrome, type <code>chrome://extensions</code> in the address bar and press Enter. In Edge use <code>edge://extensions</code>, in Brave <code>brave://extensions</code>.</li>
<li><strong>Turn on Developer mode</strong> with the switch in the top right corner.</li>
<li><strong>Click Load unpacked</strong> and choose the unzipped folder (the one that contains <code>manifest.json</code>).</li>
<li><strong>Pin the icon</strong> from the puzzle piece menu in your toolbar, so it is always one click away.</li>
</ol>"""


def faq_for(t):
    items = [
        (f"Is {t['name']} free?", "Yes. It is free to download and use, and the code is open source under the MIT license. You do not need an account, a subscription or an activation code."),
        ("Where are my results stored?", "Your scan results and settings are saved in your own browser. The extension does not ask you to sign in, and you can delete everything by removing the extension."),
        ("Which browsers does it work in?", "Google Chrome, and other browsers built on Chromium such as Microsoft Edge and Brave."),
        (t["q"], t["a"]),
        ("How do I update it?", "Download the latest zip from this page, replace the old folder with the new one, and click the reload button on the extensions page."),
    ]
    return items


def tool_page(t, tools):
    path = f"/{t['slug']}/"
    url = BASE + path
    title = f"{t['name']}: Free SEO Chrome Extension"
    if len(title) > 60:
        title = f"{t['name']} | Free Chrome Extension"
    desc = t["desc"] if len(t["desc"]) <= 150 else t["desc"][:147].rsplit(" ", 1)[0] + "."
    zipurl = f"{DL}/{t['slug']}.zip"
    faq = faq_for(t)
    sec = t["sec"]
    why = md(sec.get("Why this matters", ""))
    how = md(sec.get("How it works", "")) if sec.get("How it works") else ""
    limits = md(sec[t["limits_key"]]) if t["limits_key"] else ""
    does_title = "What it checks" if (t["does_key"] or "").endswith("checks") else "What it does"
    does_extra = re.sub(r"^- .+$", "", sec.get(t["does_key"], ""), flags=re.M).strip()
    others = [o for o in tools if o["slug"] != t["slug"]]
    perms_rows = "".join(f"<tr><th>{esc(p)}</th><td>{esc(PERMS.get(p, ''))}</td></tr>" for p in t["perms"])
    perms_rows += "<tr><th>Access to websites</th><td>Load the pages of the site you scan, the same way a crawler does.</td></tr>"

    schema = {"@context": "https://schema.org", "@graph": [
        website_node(), AUTHOR,
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": url + "#app"},
         "primaryImageOfPage": f"{BASE}/images/{t['slug']}-1200.jpg", "breadcrumb": {"@id": url + "#breadcrumb"},
         "inLanguage": "en", "dateModified": TODAY},
        {"@type": "SoftwareApplication", "@id": url + "#app", "name": t["name"], "description": t["intro"] or desc,
         "url": url, "applicationCategory": "BrowserApplication", "applicationSubCategory": "SEO tool",
         "operatingSystem": "Google Chrome, Microsoft Edge, Brave", "softwareVersion": t["version"],
         "downloadUrl": zipurl, "isAccessibleForFree": True,
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
         "image": f"{BASE}/images/icons/{t['slug']}.png", "screenshot": f"{BASE}/images/{t['slug']}-1200.jpg",
         "featureList": t["features"], "permissions": ", ".join(t["perms"] + ["access to websites you scan"]),
         "author": {"@id": BASE + "/#author"}, "publisher": {"@id": BASE + "/#author"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "SEO Chrome Extensions", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": t["name"], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}

    body = f"""<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="{BASE}/">SEO Chrome Extensions</a> / <span aria-current="page">{esc(t['name'])}</span></nav></div>
<section class="hero"><div class="wrap hero-grid">
<div>
<img class="icon" src="{BASE}/images/icons/{t['slug']}.png" alt="" width="64" height="64">
<h1>{esc(t['name'])}</h1>
<p class="phrase">{esc(t['phrase'])}, free, right in your browser.</p>
<p class="lead">{esc(t['intro'])}</p>
<div class="actions"><a class="btn main" href="{zipurl}">Download free (zip)</a><a class="btn alt" href="#install">How to install</a></div>
<p class="small">Version {esc(t['version'])} for Chrome, Edge and Brave. No account needed.</p>
</div>
<figure>
<picture><source type="image/webp" srcset="{BASE}/images/{t['slug']}-800.webp 800w, {BASE}/images/{t['slug']}-1200.webp 1200w" sizes="(max-width: 860px) 100vw, 600px">
<img src="{BASE}/images/{t['slug']}-1200.jpg" alt="{esc(t['name'])} showing the results of a scan" width="1200" height="{img_h(t['slug'])}" fetchpriority="high"></picture>
<figcaption>{esc(t['name'])} after a scan of an example site.</figcaption>
</figure>
</div></section>

<section class="band alt"><div class="wrap two">
<div><h2>Why this matters</h2>{why}</div>
<div><h2>{does_title}</h2>{md(does_extra) if does_extra else ''}<ul class="checks">{''.join(f'<li>{md(f)[3:-4]}</li>' for f in t['features'])}</ul></div>
</div></section>

{f'<section class="band"><div class="wrap narrow"><h2>How it works</h2>{how}</div></section>' if how else ''}

<section class="band{' alt' if how else ''}" id="install"><div class="wrap narrow">
<h2>How to install {esc(t['name'])}</h2>
<p>It takes about a minute. You only do this once.</p>
{install_steps(t['slug'] + '.zip', t['slug'])}
<p style="margin-top:1.5rem"><a class="btn main" href="{zipurl}">Download {esc(t['name'])}</a></p>
</div></section>

{f'<section class="band{"" if how else " alt"}"><div class="wrap narrow"><h2>Good to know</h2>{limits}</div></section>' if limits else ''}

<section class="band"><div class="wrap narrow">
<h2>What the permissions are for</h2>
<p>Chrome shows these when you install. Here is what each one is used for.</p>
<table class="perm"><tbody>{perms_rows}</tbody></table>
</div></section>

<section class="band alt" id="faq"><div class="wrap narrow">
<h2>Questions</h2>
{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in faq)}
</div></section>

<section class="band"><div class="wrap">
<h2>More free SEO extensions</h2>
<ul class="grid">{''.join(card(o) for o in others)}</ul>
</div></section>"""
    return page(title, desc, path, t["slug"], schema, body)


def img_h(slug):
    from PIL import Image
    return Image.open(f"images/{slug}-1200.jpg").size[1]


def card(t):
    return (f'<li><a class="card" href="{BASE}/{t["slug"]}/"><img src="{BASE}/images/icons/{t["slug"]}.png" alt="" '
            f'width="48" height="48" loading="lazy"><div><h3>{esc(t["name"])}</h3><p>{esc(t["card"])}</p></div></a></li>')


HOME_FAQ = [
    ("Are these extensions really free?", "Yes. All seven are free to download and use and open source under the MIT license, with no account, no subscription and no activation code."),
    ("Do I need to be an SEO expert?", "No. Each tool explains what it found in plain words and shows which pages need attention first. You can also export Excel and PDF reports to share with a developer."),
    ("Where does my data go?", "Scan results and settings are saved in your own browser. The extensions do not ask you to sign in."),
    ("Which browsers are supported?", "Google Chrome, and browsers built on Chromium such as Microsoft Edge and Brave."),
    ("Can I install all seven at once?", "Yes. Download the all-in-one zip, unzip it, and load each folder with Load unpacked."),
]


def home(tools):
    title = "Free SEO Chrome Extensions for Technical SEO Audits"
    desc = "Seven free Chrome extensions for technical SEO: orphan pages, click depth, canonical chains, crawl budget, the 2MB limit, cache and security audits."
    schema = {"@context": "https://schema.org", "@graph": [
        website_node(), AUTHOR,
        {"@type": "CollectionPage", "@id": BASE + "/#webpage", "url": BASE + "/", "name": title, "description": desc,
         "isPartOf": {"@id": BASE + "/#website"}, "mainEntity": {"@id": BASE + "/#tools"},
         "primaryImageOfPage": BASE + "/images/og/home.jpg", "inLanguage": "en", "dateModified": TODAY},
        {"@type": "ItemList", "@id": BASE + "/#tools", "name": "Free SEO Chrome extensions", "numberOfItems": len(tools),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/{t['slug']}/", "name": t["name"]}
                             for i, t in enumerate(tools)]},
        {"@type": "FAQPage", "@id": BASE + "/#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HOME_FAQ]},
    ]}
    body = f"""<section class="hero"><div class="wrap hero-grid">
<div>
<h1>Free SEO Chrome extensions for technical audits</h1>
<p class="lead">Seven small tools that each check one part of your site: orphan pages, click depth, canonical chains, crawl budget, page size, caching and security. They show you exactly which pages need fixing, and let you export the results to Excel or PDF.</p>
<div class="actions"><a class="btn main" href="{DL}/chrome-extensions-all.zip">Download all seven (zip)</a><a class="btn alt" href="#tools">Choose one tool</a></div>
<p class="small">Free for Chrome, Edge and Brave. No account, no subscription.</p>
</div>
<figure>
<picture><source type="image/webp" srcset="{BASE}/images/orphan-page-finder-800.webp 800w, {BASE}/images/orphan-page-finder-1200.webp 1200w" sizes="(max-width: 860px) 100vw, 600px">
<img src="{BASE}/images/orphan-page-finder-1200.jpg" alt="Orphan Page Finder showing orphan, weakly linked and well linked pages" width="1200" height="{img_h('orphan-page-finder')}" fetchpriority="high"></picture>
<figcaption>Orphan Page Finder, one of the seven tools, after a scan.</figcaption>
</figure>
</div></section>

<section class="band alt" id="tools"><div class="wrap">
<h2>The tools</h2>
<p>Pick the one for the problem you are working on. Each page explains what the tool checks and how to install it.</p>
<ul class="grid">{''.join(card(t) for t in tools)}</ul>
</div></section>

<section class="band"><div class="wrap two">
<div><h2>Why use these instead of a crawler?</h2>
<p>Big SEO crawlers are great, but they cost money, take time to set up, and show you hundreds of numbers at once. These extensions do one job each. Open your site, click the icon, and you get a clear answer to one question.</p>
<p>Because they run inside your browser, there is nothing to install on your server and nothing to configure. Some of them can even read links on pages that only show them with JavaScript.</p></div>
<div><h2>What they have in common</h2><ul class="checks">
<li>Free, with no account or activation code</li>
<li>Export to Excel and PDF, ready to share with a developer or client</li>
<li>Keep your data in your own browser</li>
<li>The crawling tools keep working in the background and save their progress</li>
<li>Clear results in plain words, not hundreds of numbers</li>
</ul></div>
</div></section>

<section class="band alt" id="install"><div class="wrap narrow">
<h2>How to install</h2>
<p>The steps are the same for every tool, and take about a minute.</p>
{install_steps('chrome-extensions-all.zip', None)}
<p class="note" style="margin-top:1.5rem">Developer mode only means Chrome lets you load an extension from a folder on your computer. It does not change anything else in your browser.</p>
</div></section>

<section class="band" id="faq"><div class="wrap narrow">
<h2>Questions</h2>
{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in HOME_FAQ)}
</div></section>

<section class="band alt"><div class="wrap narrow">
<h2>Who made these</h2>
<p>These extensions are built and maintained by <a href="https://mmseo.app/">MM Rahman Bappi</a>, a technical SEO consultant and web developer with 15 years of experience. They started as tools for client audits and are now free for everyone.</p>
<p>Found a bug or have an idea? <a href="{REPO}/issues">Open an issue on GitHub</a>.</p>
</div></section>"""
    return page(title, desc, "/", "home", schema, body)


def not_found():
    schema = {"@context": "https://schema.org", "@graph": [website_node()]}
    body = f"""<section class="hero"><div class="wrap narrow"><h1>Page not found</h1><p class="lead">This page does not exist or has moved.</p><p><a class="btn main" href="{BASE}/">See all tools</a></p></div></section>"""
    return page("Page not found | Free SEO Chrome Extensions", "This page does not exist.", "/404.html", "home", schema,
                body).replace('content="index, follow, max-image-preview:large"', 'content="noindex, follow"')


def main():
    tools = load_tools()
    open("site.css", "w").write(CSS.strip() + "\n")
    open("index.html", "w").write(home(tools))
    for t in tools:
        os.makedirs(t["slug"], exist_ok=True)
        open(f"{t['slug']}/index.html", "w").write(tool_page(t, tools))
    open("404.html", "w").write(not_found())
    urls = [BASE + "/"] + [f"{BASE}/{t['slug']}/" for t in tools]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                   + "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n" for u in urls)
                                   + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    open("favicon.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#16835a"/>'
                                   '<path d="M18 40l9-9 7 6 12-15" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>\n')
    open(".nojekyll", "w").write("")
    print("built", len(tools) + 2, "pages")


if __name__ == "__main__":
    main()
