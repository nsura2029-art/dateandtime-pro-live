# dateandtime.live — Landing Page

The home page of [tdp-landing-dev.nsura2029.workers.dev](https://tdp-landing-dev.nsura2029.workers.dev/) — a single self-contained `index.html` for the Cloudflare Worker that serves the marketing/landing experience.

## What's in here

- **`index.html`** — the landing page (3,788 lines, ~229 KB). Single file, all CSS inlined, no build step. Drop it into the Worker at the right route and it works.
- **`build.py`** — the transform script that produced `index.html`. Strips old CSS from the source, injects the design system tokens, splices site-specific component CSS, leaves all DOM/JS/IDs/JSON-LD intact. Run it when the design system reference or the source HTML changes.
- **`validate.py`** — Playwright check. Loads the page in both `color_scheme=light` and `color_scheme=dark`, asserts `data-theme` flips, all 17 sections render, no internal 404s, no console errors. Run before every commit.
- **`.gitignore`** — keeps validation artifacts (`imgs/_*.png`) and Python junk out of the repo.

## Design system

The page uses the Meilisearch-style design system defined in `dateandtime-design.html` (kept outside this repo as the reference). Token categories: color, type, spacing, radius, shadow, layout, motion. Light + dark via `[data-theme="..."]` overrides. No CSS hard-coded in component styles — everything uses `var(--color-*)`, `var(--space-*)`, etc.

## Sections (17 + header + footer)

1. Hero with live UTC clock, format toggle, sync indicator, DST countdown
2. Pills row (holiday, on-this-day, working hours, sunrise/sunset, DST)
3. Big mono clock
4. Favorite cities rail (home + 5 most-recent)
5. Search box + popular cities
6. Today on Earth (6 cities with live time)
7. Time tools grid (World Clock, Meeting Planner, Converter, Zones)
8. Knowledge base chip cloud
9. Today's snapshot (4 cards)
10. Long weekend finder (country select)
11. Did you know?
12. Famous birthdays (deceased)
13. Celebrity birthdays (living)
14. Famous deaths
15. Year timeline
16. On this day
17. FAQ
+ Continue your journey
+ Footer (with cookie banner + feedback widget)

## API endpoints the page calls

- `/api/v1/cities` — search
- `/api/v1/time/now` — server time check
- `/api/v1/time/sun` — sunrise/sunset
- `/api/v1/onthisday` — today's events
- `/api/v1/holidays` — holidays
- `/api/v1/dst/upcoming` — DST changes
- `/api/v1/cities/:id/climate` — climate
- `/api/v1/cities/:id/aliases` — historical names
- `/api/v1/countries/:cca2/working-hours` — business hours
- `/api/v1/feedback` — feedback widget

Base URL switches between `https://api.dateandtime.live` (prod) and `https://dev.api.dateandtime.live` (dev) automatically based on `location.hostname`.

## External scripts

The page loads three scripts that live next to `index.html` in the Worker (typically in `home_files/`):

- `site-shell.js` — theme toggle, mobile nav, sticky header
- `api-data.js` — client-side data cache
- `cookie-consent.js` — cookie consent banner

These aren't in this repo because they live alongside the Worker file system.

## Local development

```bash
# Validate
python3 validate.py

# Rebuild from a new source/reference
python3 build.py
```

Validation needs Playwright + Chromium:

```bash
playwright install chromium
```

## Deployment

This file is designed to live in a Cloudflare Worker. The Worker serves it at the root route, and the supporting `home_files/` directory sits next to it. See the Worker config for the exact setup.

## Changelog

- `1ac7e35` — section-update: FAQ section (added eyebrow, subtitle, data-reveal)
- `8c6c9c2` — full redesign with the design system
- `v1.0` — tag for the design-system milestone
