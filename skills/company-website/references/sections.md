# Page Sections & Copy

Order follows how visitors decide: *what is this → can they help me → can I trust them → how do I reach them.*

## 1. Header
Logo/name, 4–5 anchor links, language toggle, one primary CTA button (WhatsApp or "Get a quote"). Sticky on scroll, collapses to a menu button below 760px.

## 2. Hero
- **Headline** (≤ 10 words): the outcome the customer gets, not the company name.
  - ✗ "Welcome to Nile Tech" → ✓ "IT that keeps your business running"
- **Subheadline** (1–2 lines): who you serve + what you do.
- **Primary CTA** + secondary CTA (e.g. "Our services").
- Optional trust line: years in business, number of clients — only if the user gave real numbers.

## 3. Services
3–6 cards: icon, title (2–4 words), one sentence of benefit. Link to contact with the service preselected if useful.

## 4. About
2 short paragraphs: story/mission and what makes you different. Optional photo of the team.

## 5. Why Us
3–4 points with short proof (licensed, fast response, warranty, local team). No unverifiable claims.

## 6. Work / Clients (optional)
Only real projects or logos the user provides, with permission.

## 7. Testimonials (optional)
Only real quotes with name and role/company. Never generate fake reviews.

## 8. FAQ (optional)
4–6 questions customers actually ask (pricing approach, coverage area, timelines). Use `<details>`/`<summary>`.

## 9. Contact
Phone, WhatsApp, email, address, working hours, map link. Simple form (name, phone, message). The template sends the form to WhatsApp, or opens an email if no WhatsApp number is set.

## 10. Footer
Name, short line, quick links, social links, © year (auto-filled).

## Copy Guidelines

- Write each language natively; don't translate word for word. Arabic copy should read like Modern Standard Arabic or the audience's preferred dialect, as the user decides.
- Short sentences, active voice, "you" focused.
- Every section ends with a reason to contact.
- Use real numbers only; mark missing ones `[ADD …]`.

## Multi-page sites

If the user needs separate pages (e.g. one per service, blog, careers), copy `index.html` to `services/<slug>.html`, keep the same header/footer, update `<title>`, meta description and canonical URL, and add each page to `sitemap.xml`.
