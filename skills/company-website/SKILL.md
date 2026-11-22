---
name: company-website
description: Design, build, check and launch a professional company / business website (landing page, services, about, contact) with Arabic (RTL) and English support. Use when the user says "build a website for my company", "design my business site", "make a landing page for my company", "اعمل موقع لشركتي", "صمم موقع اليكتروني", or "launch my company website".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <company-name>
---

# Company Website

Build a fast, accessible, bilingual (Arabic RTL / English LTR) company website from a short brief, then verify and deploy it. The output is a dependency-free static site (HTML + CSS + a little JS) that runs anywhere and deploys to Vercel in one command.

## How It Works

1. **Collect the brief** – ask the user the intake questions below (skip any they already answered).
2. **Scaffold** – run `scaffold.sh` to generate the site from the bundled template with the company's details filled in.
3. **Design** – adjust brand colors, fonts, copy and sections using [references/design-system.md](references/design-system.md) and [references/sections.md](references/sections.md).
4. **Check** – run `check-site.sh` to catch SEO, accessibility and broken-link problems; fix every error.
5. **Preview** – serve locally (`python3 -m http.server`) and review on desktop and phone widths.
6. **Launch** – deploy with the `vercel-deploy` skill, then walk the user through [references/launch-checklist.md](references/launch-checklist.md) (domain, analytics, forms, Search Console).

## Intake Questions

Ask in the user's language. Keep it to one message:

1. Company name (and Arabic name if different)
2. One-line description: what you do and for whom
3. Main services / products (3–6 items, one line each)
4. Primary language: Arabic, English, or both (default: both, Arabic first)
5. Brand color (hex) or logo file — if none, propose a palette from the design system
6. Contact info: phone / WhatsApp, email, address, social links
7. Main goal of the site: calls, WhatsApp messages, quote requests, store visits, bookings

Never invent phone numbers, addresses, client logos, testimonials or statistics. Leave clearly marked placeholders (`[ADD …]`) and tell the user which ones remain.

## Usage

```bash
bash /mnt/skills/user/company-website/scripts/scaffold.sh <output-dir> [config.json]
bash /mnt/skills/user/company-website/scripts/check-site.sh <site-dir>
```

**Arguments:**
- `output-dir` - Where to create the site (must not exist or must be empty)
- `config.json` - Company details (optional; placeholders are kept for missing fields)
- `site-dir` - Site folder to audit (defaults to current directory)

**Config format** (all fields optional):

```json
{
  "name": "Nile Tech",
  "nameAr": "نايل تك",
  "tagline": "IT solutions for growing businesses",
  "taglineAr": "حلول تقنية للشركات النامية",
  "primaryColor": "#0f766e",
  "phone": "+20 100 000 0000",
  "whatsapp": "201000000000",
  "email": "info@example.com",
  "address": "Cairo, Egypt",
  "addressAr": "القاهرة، مصر",
  "defaultLang": "ar",
  "siteUrl": "https://example.com"
}
```

**Examples:**

```bash
# Scaffold with placeholders, then edit by hand
bash /mnt/skills/user/company-website/scripts/scaffold.sh ./my-company-site

# Scaffold from a brief
bash /mnt/skills/user/company-website/scripts/scaffold.sh ./site ./company.json

# Audit, then deploy
bash /mnt/skills/user/company-website/scripts/check-site.sh ./site
bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh ./site
```

## Generated Site

```
site/
  index.html     # Hero, services, about, why-us, contact, footer (AR + EN)
  styles.css     # Design tokens, RTL-aware layout, dark mode
  script.js      # Language toggle, mobile menu, year, contact form → WhatsApp/email
  robots.txt
  sitemap.xml
  favicon.svg
  404.html
```

Bilingual text uses `data-ar` / `data-en` attributes; the toggle swaps text, `lang` and `dir` and remembers the choice. To make a single-language site, set `defaultLang` and remove the toggle button.

## Output

`scaffold.sh` prints progress to stderr and JSON to stdout:

```json
{"siteDir":"/abs/path/site","files":7,"placeholders":["[ADD phone]"]}
```

`check-site.sh` prints findings and a JSON summary:

```
ERROR index.html: <img> missing alt text (line 42)
WARN  index.html: placeholder text remains: [ADD phone]
{"errors":1,"warnings":1,"files":2}
```

Exit code is non-zero when there are errors.

## Present Results to User

```
✓ Website ready: <company name>

Pages/sections: Hero · Services · About · Why us · Contact
Languages: العربية / English
Checks: 0 errors, N warnings

Still needed from you:
- [list of remaining placeholders]

Next steps:
1. Preview: <preview URL>
2. Claim it on your Vercel account: <claim URL>
3. Connect your domain (see launch checklist)
```

## Design Rules (summary)

- Mobile first; one clear call to action per section (WhatsApp/call/quote).
- Max 2 fonts. Arabic: "IBM Plex Sans Arabic", "Cairo" or "Tajawal"; English: "Inter".
- Use logical CSS properties (`margin-inline-start`, `inset-inline-end`) so RTL works automatically.
- Contrast ≥ 4.5:1, visible focus states, `alt` on every image, real `<button>`/`<a>` elements.
- Keep pages light: compressed WebP/AVIF images with `width`/`height`, `loading="lazy"` below the fold.

For a full UI audit, also run the `web-design-guidelines` skill. If the user wants a React/Next.js site instead, follow `react-best-practices`.

## Troubleshooting

- **`output-dir is not empty`** – pick a new folder or remove the old one.
- **`python3 is required`** – both scripts use Python 3 (standard library only); install it and retry.
- **Arabic text shows as boxes** – make sure the Google Fonts `<link>` is present and the network allows `fonts.googleapis.com`.
- **Deployment blocked (claude.ai)** – add `*.vercel.com` at `claude.ai/settings/capabilities`, then retry.
- **Contact form does nothing** – static sites have no backend; the template sends the message to WhatsApp or opens an email. For stored submissions, see the forms section of the launch checklist.
