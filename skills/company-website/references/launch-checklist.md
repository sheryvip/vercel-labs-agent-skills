# Launch & Operations Checklist

Walk the user through these after the first deployment. Mark what is done.

## Before launch
- [ ] `check-site.sh` reports 0 errors, and no `[ADD …]` placeholders remain
- [ ] Phone, WhatsApp, email links tested on a real phone
- [ ] Every page has a unique `<title>` (≤ 60 chars) and meta description (≤ 160 chars)
- [ ] `siteUrl` set so canonical, Open Graph and `sitemap.xml` use the real domain
- [ ] Favicon and social share image (`og-image.png`, 1200×630) added
- [ ] Privacy note if you collect any personal data

## Hosting & domain (Vercel)
1. Deploy with the `vercel-deploy` skill. It returns a Preview URL and a Claim URL.
2. Open the **Claim URL** and sign in to move the project to the user's own Vercel account (free Hobby plan is fine for a company brochure site; commercial use may require Pro, so check Vercel's current terms).
3. Project → **Settings → Domains** → add `example.com` and `www.example.com`.
4. At the domain registrar, add the DNS records Vercel shows (usually an `A` record to `76.76.21.21` and a `CNAME` for `www` to `cname.vercel-dns.com`). HTTPS is automatic.
5. For future updates: connect the project to a GitHub repo so every push redeploys, or re-run the deploy script.

## Forms (stored submissions)
The template's form sends to WhatsApp or email. Use one of these if submissions need to be stored:
- Form service (Formspree, Basin, Web3Forms): set the form `action` to the service endpoint and `method="POST"`, then remove the JS handler.
- Own backend: a Vercel Function (`api/contact.js`) that emails or saves to a database.

## Analytics & search
- [ ] Enable **Vercel Web Analytics** (Project → Analytics), or add Google Analytics / Plausible
- [ ] Verify the domain in **Google Search Console** and submit `sitemap.xml`
- [ ] Create or update the **Google Business Profile** with the same name, address and phone (NAP)
- [ ] Add the site link to all social profiles

## Ongoing maintenance (monthly)
- Update services, prices, photos and team
- Check that forms and WhatsApp links still work
- Review analytics: top pages, where visitors drop off, CTA clicks
- Re-run `check-site.sh` after every content change
- Renew the domain before it expires (turn on auto-renew)
