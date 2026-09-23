# Free SEO Chrome Extensions

![Seven free SEO Chrome extensions](images/og/home.jpg)

Seven free Chrome extensions for technical SEO. Each one checks one part of your site and shows you exactly which pages need fixing. You can export every result to Excel or PDF.

Website: https://mmrahmanbappi.github.io/seo-chrome-extensions/

## The tools

| Tool | What it does | Get it |
|---|---|---|
| [Orphan Page Finder](https://mmrahmanbappi.github.io/seo-chrome-extensions/orphan-page-finder/) | Finds pages in your sitemap that no internal link points to. | [Download](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/orphan-page-finder.zip) |
| [Click Depth Mapper](https://mmrahmanbappi.github.io/seo-chrome-extensions/click-depth-mapper/) | Shows how many clicks each page is from your homepage. | [Download](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/click-depth-mapper.zip) |
| [Canonical Chain Tracer](https://mmrahmanbappi.github.io/seo-chrome-extensions/canonical-chain-tracer/) | Follows canonical tags and finds chains and loops. | [Download](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/canonical-chain-tracer.zip) |
| [Crawl Budget Waste Finder](https://mmrahmanbappi.github.io/seo-chrome-extensions/crawl-budget-waste-finder/) | Finds filter, tracking and session URLs that waste crawl budget. | [Download](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/crawl-budget-waste-finder.zip) |
| [Two MB Crawl Limit Monitor](https://mmrahmanbappi.github.io/seo-chrome-extensions/two-mb-crawl-limit-monitor/) | Finds pages close to or over Googlebot's 2MB crawl limit. | [Download](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/two-mb-crawl-limit-monitor.zip) |
| [Full Site Cache Auditor](https://mmrahmanbappi.github.io/seo-chrome-extensions/full-site-cache-auditor/) | Runs 54 checks on caching, CDN and DNS. | [Download](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/full-site-cache-auditor.zip) |
| [Full Site Security Auditor](https://mmrahmanbappi.github.io/seo-chrome-extensions/full-site-security-auditor/) | Runs 47 security, DNS and CMS checks. | [Download](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/full-site-security-auditor.zip) |

Want all seven? [Download them in one zip](https://github.com/mmrahmanbappi/seo-chrome-extensions/releases/latest/download/seo-chrome-extensions-all.zip).

## How to install

1. Download the zip for the tool you want and unzip it.
2. In Chrome, go to `chrome://extensions` (in Edge `edge://extensions`, in Brave `brave://extensions`).
3. Turn on **Developer mode** in the top right corner.
4. Click **Load unpacked** and choose the unzipped folder, the one that contains `manifest.json`.
5. Pin the icon from the puzzle piece menu so it is easy to find.

## Good to know

- Free to use, with no account, subscription or activation code
- Your results and settings are saved in your own browser
- Works in Google Chrome and other Chromium browsers such as Edge and Brave

## Found a problem?

[Open an issue](https://github.com/mmrahmanbappi/seo-chrome-extensions/issues) and describe what happened, which tool you used, and your browser version.

## About

Built and maintained by [MM Rahman Bappi](https://mmseo.app/), a technical SEO consultant and web developer with 15 years of experience.

## Updating the website

The website is built from the READMEs and manifests. After changing them, run:

```sh
python3 tools/make_images.py   # only when promo images change
python3 tools/build_site.py
```

## License

Each tool has its own LICENSE file. The tools are free to download and use.
