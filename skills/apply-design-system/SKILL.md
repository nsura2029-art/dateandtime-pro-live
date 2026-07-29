---
name: apply-design-system
description: Apply a Meilisearch-style design system to any page (home, features, pricing, docs, etc.) without changing sections, their order, or the content in each section. Use when the user wants to redesign an existing page to use a known design system — tokenized styling, responsive layout, hover treatments, mouse ambience, scroll-reveal effects — while preserving all structure and copy verbatim. Output is a single self-contained `index.html` with light + dark mode.
---

# Apply Design System

A reusable workflow for **redesigning a page with an existing design system** without touching its structure or content. Designed for the `dateandtime.live` / `tdp-landing-dev` Worker family, but the workflow generalizes to any tokenized design system + page pair.

---

## When to use this skill

Use it when the user says any of:

- "Redesign [page URL] using the design system from [reference file]"
- "Apply the design system to [page], don't change the sections"
- "Restyle [page] to match [reference], keep the content"
- "I want the same look-and-feel across all our pages"
- "Re-skin [page] with the token system"

Do **not** use it when:
- The user wants to change content or add new sections (use a normal build flow)
- There's no design system reference (use `landing-page-builder` instead)
- The user is starting from scratch with no source page

---

## Inputs

Before running, gather from the user (or read from attached files):

| Input | What it is | Where to get it |
|---|---|---|
| **Source page** | The page to redesign. Sections + content are the source of truth. | A live URL or an attached HTML file. |
| **Design system reference** | An HTML file that contains the tokens and component classes to port. | Typically `dateandtime-design.html` or similar — has `:root { --color-* }` tokens and component classes like `.card`, `.btn`, `.mini-card`. |
| **Output route** (optional) | Where the new HTML will live in the Worker. | Ask the user if not obvious from the source URL. |
| **Theme default** (optional) | Which theme to use on first visit. | Defaults to `prefers-color-scheme`; override only if the user specifies. |

---

## The prompt (paste this verbatim when running the skill in a fresh session)

```
TASK: Redesign the home page of <SOURCE_URL> using the design system from
<REFERENCE_FILE>, without changing the sections, their order, or the
content in each section.

HARD RULES — DO NOT VIOLATE
───────────────────────────
1. Sections: keep every existing <section> exactly as it is — same headings,
   same copy, same DOM order, same list items, same links. Only the visual
   layer changes.
2. Content: do not add, remove, or rewrite any text, links, CTAs, or list items
   in any section. If the reference doesn't have a component for something,
   style it with the tokens — don't invent new content.
3. Existing functionality: every piece of working behavior in the source page
   MUST keep working. This is non-negotiable. Before you build, inventory
   every API call, form submission, client-side state, event handler, fetch,
   analytics event, or third-party script the source page uses. The output
   must run all of them — same endpoints, same payloads, same error handling,
   same success paths. If the source page calls `/api/v1/cities?q=Tokyo` on
   a keystroke, the output must do the same. If the source page has a form
   that POSTs to a webhook, the output must POST to the same webhook.
4. App-level cleanup: the output is a CLEAN reimplementation, not a layered
   patch over the source's old styles. Strip out the old page's:
   - <style> blocks, <link rel="stylesheet"> tags, inline style="..."
   - Old CSS custom properties and old token names (anything the
     design system already covers)
   - Old class definitions that conflict with the new system
   - Old JS that depended on the old styles (visual-only handlers;
     behavior handlers stay, see rule 3)
   - Dead CSS (selectors that no longer match anything in the new DOM)
   - Old fonts, old favicon, old meta tags that the new design replaces
   - Old analytics / tracking tags that the new design doesn't use
   - Old comments, old TODOs, old debug code, old console.logs
   - Old whitespace patterns, old code formatting styles
   Don't carry over a single byte of the source's CSS, styling code, or
   visual scaffolding. The only thing that survives is the DOM structure,
   the content, and the working JS handlers (per rule 3). After cleanup,
   the file should look like a fresh implementation that happens to
   have the same content as the source — not a fork of the source.

   Practical rule: if the source has a <style> block at the top, delete
   the entire <style> block and start from the design system tokens.
   If the source has 5 <link rel="stylesheet">, drop them all and use
   only the Google Fonts link. If the source's <body> has 30 inline
   style="..." attributes, strip them and let the design system classes
   take over.
5. Output: a single self-contained index.html file. CSS inlined, no JS
   framework, no build step. Only external dep is Google Fonts (Inter +
   JetBrains Mono). Validate locally with Playwright, then publish a preview
   URL.

DESIGN SYSTEM — extract from <REFERENCE_FILE>
──────────────────────────────────────────────────────
Tokens (expose as CSS custom properties on :root, override under
[data-theme="light"]):

  Color     --color-bg, --color-bg-soft, --color-bg-elevated,
             --color-bg-translucent, --color-border, --color-border-strong,
             --color-fg, --color-fg-soft, --color-fg-muted,
             --color-primary, --color-primary-hover, --color-primary-soft,
             --color-accent, --color-accent-soft, --color-success
  Type      --font-sans (Inter), --font-mono (JetBrains Mono),
             --t-display/h1/h2/h3/h4/body/small/caption/eyebrow (clamp),
             --t-w-*, --t-ls-*, --t-lh-*
  Spacing   --space-1 → --space-16 (4px base)
  Radius    --radius-sm/md/lg/xl/pill
  Shadow    --shadow-sm/md/lg + --shadow-glow (uses --color-primary)
  Layout    --container-max, --container-pad, --header-h

Component classes to port from the reference (keep their DOM, swap the
visual treatment to use the tokens above):
  .site-header, .brand, .brand-mark, .nav-list, .nav-link, .lang-pill,
  .theme-toggle, .btn / .btn-primary / .btn-ghost,
  .section, .section-divider, .section-header, .section-eyebrow,
  .section-title, .section-sub,
  .hero, .hero-title, .hero-sub, .hero-demo, .hero-search, .hero-search-input,
  .hero-search-ai / .switch, .hero-demo-list / .hero-demo-item / .thumb,
  .hero-cta-row, .logo-cloud / .logo-cloud-eyebrow / .logo-cloud-list / .logo,
  .feature-grid, .card, .card-icon, .card-title, .card-desc,
  .showcase, .showcase-eyebrow, .showcase-title, .showcase-desc,
  .app-mock, .app-mock-tabs, .app-mock-tab / .dot, .app-mock-body,
  .app-mock-row / .icon,
  .feature-grid-3x3, .mini-card, .mini-card-icon, .mini-card-title,
  .mini-card-desc,
  .testimonial, .testimonial-eyebrow, .testimonial-quote, .testimonial-meta,
  .testimonial-logo, .testimonial-dots, .testimonial-dot,
  .code-section, .code-window, .code-tabs, .code-tab, .code-body,
  .code-body .kw/.str/.num/.com/.fn/.var/.punct, .code-actions,
  .stats, .stats-eyebrow, .stats-title, .stats-cta, .stats-numbers,
  .stat-num / .unit, .stat-label,
  .tokens-panel, .tokens-grid, .tokens-group-title, .color-swatches,
  .swatch / .swatch-color / .swatch-label, .type-specimens, .type-spec,
  .type-spec-meta,
  .community, .community-card, .community-card-icon, .community-card-desc,
  .site-footer, .footer-top, .footer-brand-desc, .footer-social,
  .footer-social-icon, .footer-col-title, .footer-col-list, .footer-bottom,
  .footer-bottom-actions

VISUAL LAYER — must implement
──────────────────────────────
□ Tokenized styling
  Every color, type, space, radius, shadow, layout value uses a CSS custom
  property. Zero hard-coded values in component styles. Verify by grepping
  the output for `#[0-9a-f]{3,6}` outside the :root / [data-theme] blocks.

□ Responsive layout
  3-col grids collapse to 2-col at 900px, 1-col at 560px. Nav collapses
  under 900px. Section padding tightens on mobile (--space-12 → --space-10).
  Hero search widget, showcase, stats all stack on mobile.

□ Hover treatment
  Every interactive surface (card, button, link, icon, tab, swatch) gets a
  coordinated hover state: border darkens + lift translateY(-2 to -4px) +
  shadow grows + icon scales/rotates -6 to -8°. Easing:
  cubic-bezier(0.4, 0, 0.2, 1), 200-300ms.

□ Mouse ambience (desktop only, @media (hover: hover) and (pointer: fine))
  - Custom cursor: 14-16px ring, border-only, mix-blend-mode: difference.
    Scales to 35-40px filled circle on interactive elements.
  - Mouse-follow spotlight: 500-600px radial gradient on body::after,
    tracks the pointer via rAF (~20% lerp). mix-blend-mode: screen in dark,
    multiply in light. Subtle — should feel like the page reacts to you,
    not like a flashlight.

□ Scroll-reveal
  Every section element gets data-reveal="up|left|right|scale".
  IntersectionObserver fires on entry, fades from opacity:0 + 24px offset
  to identity over 600-700ms with easeOutExpo
  (cubic-bezier(0.16, 1, 0.3, 1)).
  Cards within the same section get a time-staggered delay via
  data-stagger index × 70-90ms — they "wave" in, not all at once.

□ Time-staggered card load (explicit)
  For the 3x3 mini-card grid and the 9-swatch grid, set
  data-stagger="0..8" on each card. JS computes
  delay = baseDelay + (stagger × 70ms) and applies .is-visible so the
  cards ripple in left-to-right, top-to-bottom.

LIGHT + DARK MODE
─────────────────
- [data-theme="dark"] is the default (matches the reference).
- [data-theme="light"] overrides the color tokens only.
- Theme toggle pill in the header (sun/moon SVGs, knob slides 28px).
- Persist choice to localStorage (dt-theme).
- Default to system preference on first visit. Listen to
  prefers-color-scheme change events and follow them until the user
  picks manually.
- The body::before glow + body::after spotlight must both respect the
  theme (subtle in light, more present in dark).

WIRE-UP — keep every piece of existing behavior working
──────────────────────────────────────────────────────────
The source page has real functionality. Inventory it first (see "How to
run" step 2) and reimplement it. Do not turn real behavior into decoration.

General rule: anything the source page does, the output does. Endpoints,
payloads, side effects, error paths — all preserved.

Reference-design behaviors (re-implement these from the reference, even
if the source doesn't have them):
- Code tabs: click swaps the <pre> body to the matching snippet
  (JS / cURL / Go / Python / PHP / Java / Rust / Swift / Dart / .NET /
  Ruby / HTTP). Update the "JS — install meilisearch" label to match.
- Testimonial dots: click cycles the .active class.
- Hero "Boost my search with AI" pill: click toggles .is-on on the
  pill and animates the switch.
- Stat numbers: count up from 0 to target over 1.4s when they scroll
  into view. Use data-count-to and data-suffix attributes.
- Theme toggle: click flips data-theme on <html>, persists to
  localStorage, updates the knob transform.

Source-specific behaviors (preserve exactly — copy the handler logic,
update only the selectors to match the new DOM):
- API calls: every fetch / XHR / WebSocket. Match the URL, method,
  headers, body, query params. Update the success and error render
  functions to use the new class names.
- Forms: every <form> submit, including the preventDefault, the
  validation, the loading state, the success message, the error
  message, the redirect on success. Keep the same <input> names
  so the backend still receives the same fields.
- Event handlers: every addEventListener on the source page. Translate
  the selector from old class names to new class names. Don't drop
  any.
- Third-party scripts: if the source page loads analytics, chat
  widgets, or any external script, include them in the output with
  the same IDs/keys/positions.
- LocalStorage / sessionStorage / cookies: any key the source reads
  or writes, the output must read/write the same key. Theme
  persistence is a special case — use `dt-theme` (matches the
  design system) but if the source used a different key like
  `theme-pref`, preserve that too.
- URL params: anything the source reads from location.search or
  location.hash, the output must read the same way.
- IntersectionObserver / scroll listeners: any non-visual behavior
  (e.g. infinite scroll, lazy load, analytics on view) must be
  preserved. The new reveal observer is fine to add, but don't
  drop the source's observers.

Validation: after wiring, run a smoke test in Playwright that
exercises each handler. For a search input, type a query, press
enter, assert the API was called. For a form, fill it, submit,
assert the request fired. For a button, click, assert the side
effect. Don't ship until every handler in the inventory is
confirmed working.

A11Y + REDUCED MOTION
─────────────────────
- prefers-reduced-motion: reduce: kill all animation, transitions, the
  spotlight, and force [data-reveal] to its visible state immediately.
- Use data-hover on every interactive element so the custom cursor can
  attach via event delegation in one place.
- Keep the original semantic structure: <header>, <main> of <section>s,
  <footer>. Don't swap them for <div>s.

VALIDATION — must pass before publishing
────────────────────────────────────────
Run a Playwright script that, for BOTH color_scheme=light and
color_scheme=dark:

  1. Loads the page, asserts <html data-theme> matches the requested mode.
  2. Asserts section count equals the original page's section count.
  3. Asserts every [data-reveal] becomes .is-visible after scrolling
     the full page.
  4. Asserts the theme toggle round-trips (dark → light → dark, or vice
     versa) by clicking the [data-theme-btn].
  5. Asserts 0 failed responses, 0 console errors, 0 broken images.
  6. Saves a full-page screenshot per mode.

DELIVERABLES
────────────
- index.html (single file, inlined CSS, no external assets beyond Google
  Fonts)
- Source zip
- Public preview URL (deploy via the website_deploy tool)
- One-paragraph note confirming every original section + content was
  preserved verbatim
```

---

## How to run (after the prompt above)

There are two modes. Pick based on what the user wants.

**Mode A: Full-page redesign** — rewrite the whole `index.html` from scratch (or via the transform script for large pages). Use when the user wants a brand new look across the entire page, or when the design system is being applied to a greenfield page.

**Mode B: Section-by-section update** — touch just one section, leave everything else byte-for-byte identical. Use when the user wants to land changes incrementally, A/B test, or refresh a single component. See [Section-by-section mode](#section-by-section-mode-incremental-updates) below for the full workflow.

If the user doesn't specify, ask: "Do you want me to redesign the whole page, or just one section?"

### Mode A: Full-page workflow

1. **Read the source page** — `web_fetch <SOURCE_URL>` or read the attached HTML. Confirm the section list, copy, and links. Write them down.
2. **Read the reference** — read `<REFERENCE_FILE>`. Extract the token list and the component class catalog. Note which components the source page actually needs.
3. **Inventory existing functionality** — read the source page's `<script>` blocks and any inline event handlers. List every piece of working behavior:
   - **API calls**: every `fetch`, `XMLHttpRequest`, `axios`, `$.ajax`, `WebSocket`. Record URL, method, headers, body shape, response handler, error handler.
   - **Forms**: every `<form>` and its submit handler. Record the fields, the validation, the endpoint, the success behavior.
   - **Event handlers**: every `addEventListener`, every `onclick`, every `on...` attribute. Record the selector, the event, the action.
   - **Client-side state**: any `localStorage` / `sessionStorage` / `cookie` read or write. Record the key, the value shape, when it's read, when it's written.
   - **URL params**: any `location.search` / `location.hash` read. Record the param name and how it's used.
   - **Third-party scripts**: any `<script src=...>` to an external domain. Record the URL, the purpose, any IDs/keys.
   - **Observers**: any `IntersectionObserver`, `MutationObserver`, scroll/resize listeners. Record what they watch and what they do.
   - **Timers**: any `setInterval` / `setTimeout` that produces visible behavior.

   Write this as a checklist before you start building. Every item on it must appear in the output.
4. **Build `index.html`** in a fresh project dir (e.g. `/workspace/<page>-redesign/`). For large existing pages, use a transform script (strip old CSS, inject design system, splice) rather than rewriting. Strip every byte of the source's old styles — the output is a clean reimplementation, not a layered patch. Reimplement every item from the functionality inventory using the new class names.
5. **Validate** with Playwright in both `color_scheme=light` and `color_scheme=dark`. Use the validation checklist in the prompt above. **Plus** run a smoke test for every item in the functionality inventory — type into the search box, submit the form, click the button, read the storage key, etc.
6. **Deploy** via `website_deploy`. Capture the public URL.
7. **Zip** the project root (just `index.html` if there are no assets; include `videos/` + `imgs/` if any).
8. **Deliver** the URL + zip + one-paragraph "preserved verbatim" note that also lists the functionality inventory items that survived.
9. **Commit** the change locally (see [Commit protocol](#commit-protocol)).
10. **Post-run: update the skill** (see below).

### Mode B: Section-by-section workflow

See the dedicated section below for the full workflow. Short version:

1. Read the current `index.html`
2. Locate the target section by class/ID/index
3. Read the design system reference
4. Build the new section's DOM (keep all IDs, content, event handlers)
5. Splice the new section into the existing file (replace old, leave everything else alone)
6. Validate (target section changes, other sections unchanged)
7. Commit with a clear message about which section changed

---

## Post-run: update the skill (do this EVERY run)

The skill is a living document. Every run should leave it better. After the build is deployed and validated, spend 5 minutes updating `SKILL.md` with what you learned.

### What to capture after each run

Add or refine entries in the appropriate section:

- **New tokens discovered** — if you needed a token the reference didn't have (e.g. `--color-success-soft`, `--shadow-inset`, `--ease-spring`), add it to the token list in the prompt template.
- **New component classes** — if a source page had a section that didn't map to any reference class (e.g. a "pricing table" with 3 tiers, a "FAQ accordion", a "comparison table"), write the class for it. Add it to the component catalog with a one-line description. Next time, the skill has it.
- **New functionality patterns** — if a source page had a behavior pattern the skill didn't cover (e.g. "search box that debounces and calls an API on keystroke", "newsletter form that posts to Mailchimp", "video player that resumes from where the user left off"), add a wire-up instruction for it.
- **Validation gotchas** — if Playwright flagged something the prompt didn't anticipate (e.g. "the cursor ring covers the click target, use `pointer-events: none` in the cursor CSS"), add a check to the validation block.
- **Cleanup wins** — if a piece of source-page cruft was caught (e.g. a duplicate Google Fonts import, an unused CSS variable, a console.error on page load), add it to the "common pitfalls" list.
- **API endpoint inventory** — if a page calls a specific endpoint pattern (e.g. `/api/v1/time/now`, `/api/v1/cities?q=...`), add a short note in the WIRE-UP block so the next run knows the endpoint shape.
- **Per-page rollout tracker** — update the memory entry for the rollout. Add the page to the list with its date, source URL, and any quirks discovered.

### How to update

Don't rewrite the whole file. Make targeted edits:

```bash
# Edit in place, then verify nothing broke
edit /workspace/.skills/apply-design-system/SKILL.md
# Re-read the changed section to confirm
sed -n '200,240p' /workspace/.skills/apply-design-system/SKILL.md
# If the file got messy, the skill is now a refactor candidate
```

### When to refactor vs. patch

- **Patch** when the change is small (one new token, one new class, one validation check). Just add it to the right place.
- **Refactor** when the same thing has been added 3+ times across runs, or when the section has grown past 100 lines and the structure isn't clear anymore. Restructure into a sub-table or a callout block. Don't refactor for the sake of it — the skill should stay scannable.

### Don't bloat the skill

If you find yourself adding the same multi-paragraph note to every page-specific build, that note probably belongs in a separate "page-specific notes" sub-skill, not in the core skill. The core skill should be page-agnostic. If the dateandtime.live site grows complex enough to warrant per-page custom instructions, make a `dateandtime-live-page-notes` sub-skill that imports this one.

---

## Using the skill across multiple pages

The skill is page-agnostic. To apply the same design system across all pages of a Worker (e.g. `/`, `/features/`, `/pricing/`, `/docs/`):

- **Run the skill once per page.** Each page has its own section list, content, and links. Don't try to template-share the HTML — generate per page.
- **The design system reference stays the same** across runs. Cache the token block + component class catalog from the first run; re-apply with minimal diffs on subsequent runs.
- **Output is a single `index.html` per route.** Drop each into the Worker at the matching path:
  ```
  tdp-landing-dev/
  └── src/
      ├── index.html        ← home page (from this skill, run 1)
      ├── features/
      │   └── index.html    ← from this skill, run 2
      ├── pricing/
      │   └── index.html    ← from this skill, run 3
      └── ...
  ```
- **Per-page dev workflow:**
  1. `web_fetch` the dev page → confirm sections
  2. Diff against the previous build's section list → know what to keep verbatim
  3. Build the new `index.html`
  4. Validate in both modes
  5. Deploy preview, share with reviewer
  6. Promote to Worker on approval (replace the route's `index.html`)

- **Track per-page build state in a memory entry** so future runs know what's been done:
  ```markdown
  ### dateandtime.live — design system rollout
  - **Home page** (`/`): redesigned 2026-07-29, deployed to tdp-landing-dev. Sections: hero, features, showcase, 3x3 grid, testimonial, code, stats, tokens, community. Source: https://tdp-landing-dev.nsura2029.workers.dev/
  - **Features page** (`/features/`): not started
  - **Pricing page** (`/pricing/`): not started
  - **Docs page** (`/docs/`): not started
  ```

- **Reuse the validation script** across pages. Save it as `validate.py` in each project dir — it has no page-specific assumptions, just the test cases from the validation checklist above.

- **Reuse the `data-reveal` + `data-stagger` pattern.** Once the design system is in place on one page, copy the IntersectionObserver + rAF cursor code block verbatim into the next page. The CSS is the same; only the DOM inside changes.

---

## Section-by-section mode (incremental updates)

The full-page mode (above) rewrites the entire `index.html` in one run. That's the right call for greenfield redesigns, but it's overkill when:
- The user only wants to update one section (e.g., "redesign the hero, keep everything else")
- A page is already in production and the user wants to land changes incrementally
- The user wants to A/B test one section before committing to the rest

Section-by-section mode does exactly one section per run. The output is a small diff against the existing `index.html`, not a full rewrite.

### When to use

Use section-by-section mode when the user says any of:
- "Redesign just the hero" / "update only the FAQ" / "refresh the time tools grid"
- "Change the X section, keep the rest the same"
- "I want to see just one section redesigned first"
- "Do a section at a time"

### Inputs

- **Source page** — the existing `index.html` (the one already deployed, or the previous run's output)
- **Section selector** — which section to update. Use one of:
  - Section index: "section 5" → `.section:nth-of-type(5)` or the 5th `<section>` in DOM order
  - Section class: "the `.section--hero`" → `<section class="section section--hero">`
  - Section ID: "the `#features` section" → `<section id="features">`
  - Section purpose: "the long weekend finder" → match by h2 text or eyebrow
- **Design system reference** — same `dateandtime-design.html` (or a newer one if the user provides it)
- **Change scope** — does the user want:
  - Just the visual treatment? (keep copy, just restyle)
  - Component substitution? (e.g., swap the FAQ list for a different layout)
  - Add a new sub-component? (e.g., add a search box inside an existing section)

### Workflow

1. **Read the current `index.html`** — load the file the user wants to update.
2. **Locate the target section** — find the section by selector, class, or purpose. Note its current DOM, classes, and any IDs the JS depends on.
3. **Read the design system reference** — extract the tokens + the relevant component classes.
4. **Build the section's new DOM** — keep all IDs, all content, all event handlers. Apply the design system classes. Add `data-reveal` and `data-stagger` if visual layer is wanted.
5. **Splice the new section into the existing file** — find the target section's start/end in the source, replace the old with the new. Don't touch anything else.
6. **Validate** — load the file in Playwright, check:
   - The target section renders with the new design
   - The other sections render unchanged (visual diff or text diff)
   - All functionality in the target section still works (event handlers, API calls, state)
   - 0 internal 404s, 0 console errors
7. **Commit** — see the commit protocol below.
8. **Optional: deploy preview** — if the user wants to see it live before merging.

### What stays the same

- **Other sections** — untouched, byte-for-byte identical to the source.
- **The design system `<style>` block** — don't modify it; the new section uses the existing tokens.
- **The site-overrides `<style>` block** — only modify if the new section introduces a new component that the existing overrides don't cover. Otherwise, add the new component CSS to the same block.
- **All `<script>` blocks** — the JS in the page powers the existing functionality. The new section's event handlers must use IDs/classes that the JS already knows about, OR the JS must be updated to match. Pick whichever has fewer changes.
- **All meta, JSON-LD, hreflang, preconnect** — same.

### What changes

- Just the target section's `<section>...</section>` block in the body.
- Optionally, add a few component CSS rules to the `site-overrides` block if the new section needs them.
- Optionally, add `data-reveal` / `data-stagger` attributes for visual layer animations.

### Section-by-section workflow example

User: "Redesign just the FAQ section."

1. Read `index.html` — find `<section class="section section--faq">` at line 1281.
2. The section has 8 `<details>` items, each with a `<summary>` and a `<p>`. Keep all 8 — content is preserved verbatim.
3. Restyle: the existing `details/summary` uses bare browser styles. Add `.faq-item` classes to each, then add a `.faq-item` block in the site-overrides that uses the design system tokens (background: var(--color-bg-soft), border: 1px solid var(--color-border), border-radius: var(--radius-md), etc.).
4. Replace the section's content with the same DOM + new class names.
5. Validate: section renders, all 8 items still expand/collapse, no other section changed.
6. Commit: `git commit -m "redesign: FAQ section with design system tokens"`.
7. Show the diff to the user. They confirm or iterate.

### How to handle the visual layer on a single section

When the user asks for visual layer (mouse ambience, scroll-reveal) on just one section:

- **Scroll-reveal**: add `data-reveal="up"` to the section's wrapping `<section>` element. The IntersectionObserver in the JS will pick it up automatically.
- **Time-stagger**: if the section has a grid of cards, add `data-stagger="0..N"` to each card. The JS uses these indices to compute the stagger delay.
- **Custom cursor**: works globally via event delegation. If the section has interactive elements, add `data-hover` to them.
- **Mouse-follow spotlight**: works globally. No per-section work needed.

### Section-by-section vs full-page — which to pick

| Scenario | Use |
|---|---|
| User wants to redesign the whole page from scratch | **Full-page** |
| User has a live page in production and wants to land one change at a time | **Section-by-section** |
| User wants to A/B test a section before committing | **Section-by-section** |
| User wants to swap one component for another (e.g., different card layout) | **Section-by-section** |
| User wants a brand new page from a spec | **Full-page** (with `landing-page-builder`) |
| User is iterating on the design system itself (e.g., changing the gold accent) | **Full-page** |

If unsure, ask: "Do you want me to redesign the whole page, or just one section?"

### When section-by-section is wrong

- The change to one section requires updating the design system tokens themselves (e.g., the user wants the gold accent to be a different color) — that affects every section, so use full-page.
- The new section's DOM requires the JS to be updated (e.g., the existing JS handler doesn't support the new component). That's a bigger change — use full-page so the JS can be updated consistently.
- The page has a problem that affects every section (e.g., broken layout, wrong font, accessibility issue) — fix once, in the design system, applies everywhere.

---

## Commit protocol

Every section-by-section or full-page run should end with a commit. The commit captures the change, the rationale, and a pointer back to the skill run that produced it.

### Local git (in `/workspace/<project>/`)

```bash
cd /workspace/<project>  # e.g., tdp-home-final

# If not already a git repo
git init
git remote add origin <user's git URL>  # if they provided one

# Track all changes
git add -A

# Commit with a structured message
git commit -m "redesign: <page> via apply-design-system skill

- Source: <source URL or file>
- Reference: <reference file>
- Sections changed: <list of sections>
- Sections preserved: <list of preserved sections>
- Functionality inventory: <number of items preserved>
- Validation: light ✓ dark ✓
- Skill run: <date>

Co-authored-by: Mavis <noreply@minimax.io>"
```

### Critical git rules

- **Use `git add -A` (or `git add -A && git commit`)** — not `git commit -a`. `-a` only stages modifications to tracked files; it misses new untracked files. Always use `-A` first.
- **Verify before pushing**: `git show --stat HEAD` after every commit. Confirm the diff matches what you intended.
- **One commit per skill run** — don't split a run across multiple commits. The commit = the change.
- **Don't commit the validation screenshots** — they're in `imgs/_*.png`. Add them to `.gitignore` so they don't pollute the repo.

### Commit message structure

Every commit message should include:
1. **The action**: `redesign:` / `section-update:` / `fix:` / `cleanup:`
2. **The page**: `home` / `features` / `pricing`
3. **A summary line** of what changed
4. **A body** with:
   - Source of the change (URL or file)
   - Reference used (design system file)
   - Sections changed vs preserved
   - Validation result
   - Any caveats (e.g., "1 functionality handler rewritten because old class names didn't match")

### Example commit history

```
abc1234 redesign: home page via apply-design-system skill
def5678 section-update: FAQ section on home page
ghi9012 redesign: features page via apply-design-system skill
jkl3456 fix: city rail click handler after section-update
mno7890 redesign: pricing page via apply-design-system skill
```

The history shows the design system rollout: full page, then per-section refinements, then the next page. Easy to see what was done, when, and in what order.

### If the user hasn't given you a git URL

You can still:
- `git init` in the local project dir
- Make local commits
- Show the commit log + diffs to the user
- Have them push to their actual repo

Tell the user: "I've committed the change locally to `/workspace/<project>/`. Push it to your repo when you're ready — give me the URL and I'll push it for you, or run `git push` yourself."

### Pushing to a remote

If the user gave a git URL (e.g., `https://github.com/tdp/landing-page`):

```bash
git remote add origin <url>
git push -u origin main  # or whatever the default branch is
```

If push fails (auth, permissions, etc.), report the error and ask the user to push themselves.

### Tagging releases

When a full page is redesigned and validated, tag it:

```bash
git tag -a v1.0-home-redesign -m "Home page redesigned with design system"
git push origin v1.0-home-redesign
```

Tags give the user a named rollback point. If they don't like the new design, they can checkout the tag.

### .gitignore template

For a typical apply-design-system project:

```gitignore
# Validation artifacts
imgs/_*.png
validate.py
live_check.py
full_shot.py
build.py
*.pyc
__pycache__/

# OS junk
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/
*.swp
```

`build.py` and `validate.py` are useful but they're not part of the deliverable. The user only needs `index.html` to ship to the Worker. Keep the scripts in the project dir for next time, but don't push them to the repo.

---

## Workspace cleanup protocol (separate from app-level cleanup)

The HARD RULE 4 in the prompt template is about **app-level cleanup** — stripping
old CSS and styles from the page being redesigned. This section is about
**workspace cleanup** — keeping the `/workspace/` directory and the drive tidy
so dead artifacts don't pile up. Different concept, different actions.

After every redesign run, do a sweep so the workspace doesn't accumulate
dead artifacts.

### What to keep

- The **latest** project dir per route (e.g. only the most recent `/workspace/tdp-home-redesign/`)
- The **latest** source zip per route (e.g. `/workspace/tdp-home-redesign-source.zip`)
- The **latest** deployed preview URL (older ones can stay as rollback, but tag them)

### What to delete

- Old project dirs that aren't the current build
- Old zips superseded by the new one
- Old preview deployments once the new one is approved
- Old `validate.py` / `live_check.py` copies (keep one per project, not multiple)

### Cleanup commands

```bash
# 1. List what's in the workspace
ls -la /workspace/ | grep -E '-(redesign|final|source)\.zip$|/$'

# 2. Pick the project dirs to KEEP (most recent of each route).
#    Delete the rest. Example — keep tdp-final, drop tdp-redesign:
rm -rf /workspace/tdp-redesign
rm -f /workspace/tdp-redesign-source.zip

# 3. Old preview URLs (drive website nodes). List them:
mavis drive files list --category=images --source=AgentDeliverable
# (filter to the ones that look like previews)
# Then delete the old ones:
mavis drive files delete --node_id=<old_preview_node_id>
```

### Workspace hygiene rules

- **One project dir per route.** Don't keep side-by-side "v1" and "v2" dirs. If v2 replaces v1, delete v1 the moment v2 is deployed.
- **Zips mirror the current build only.** Re-zip after every successful build. Old zips are noise.
- **Drive nodes are cheap, but a list of 20+ preview URLs is not.** Delete previews once a new one ships. If you need a rollback, keep one tagged clearly (`tdp-home-preview-v1`).
- **Validation scripts**: keep `validate.py` in the project dir. Delete ad-hoc `live_check.py` and `full_shot.py` after you've captured the screenshots.
- **Screenshots**: full-page PNGs from validation runs end up in `imgs/_*.png`. After the run, copy the ones you actually need into a "shipped" folder, then clean the rest. Don't ship 30MB of validation screenshots in the source zip.
- **Local file size budget**: the source zip should be under 5MB for a single-file HTML or under 25MB if it includes video assets. If it's bigger, check for cruft.

---

## Common pitfalls

1. **Inventing new content.** The reference doesn't have a stat card? Don't add one. Style the existing structure with the closest tokenized primitive.
2. **Hard-coded colors.** The tokenization is the whole point. If you write `color: #fff` in a component, you've broken the design system. Grep your output.
3. **Re-declaring the tokens per page.** The token block is the same across pages. Copy it once, paste it at the top of every `index.html`. Don't try to refactor it into a shared file unless the Worker supports it.
4. **Forgetting `data-hover`.** The custom cursor attaches via event delegation on `[data-hover]`. If you add an interactive element without `data-hover`, the cursor won't react to it.
5. **Blocking scroll on iOS.** The mouse-follow spotlight uses `body::after` with `position: fixed`. Test on a mobile viewport — if it causes repaints, hide it under `@media (max-width: 900px)`.
6. **Not validating in both modes.** The light/dark token overrides are easy to miss. Always run the Playwright check on both `color_scheme=light` and `color_scheme=dark`.
7. **Re-deploying the same URL twice.** Each `website_deploy` creates a new drive node and a new URL. If you re-deploy without deleting the old node, you get orphan URLs. Delete the old one first.

---

## Reference output structure

A successful run produces:

```
/workspace/<route>-redesign/
├── index.html          ← single file, inlined CSS, the deliverable
├── validate.py         ← Playwright check for both modes (kept for next run)
└── imgs/               ← optional, only validation screenshots you actually need
    └── _val.png

/workspace/<route>-redesign-source.zip   ← drop into Worker at the matching route
```

Plus:
- A public preview URL from `website_deploy`
- A short note in chat: "Sections preserved: [list]. Tokens ported: [count]. Validation: light ✓ dark ✓"
- An entry in the per-page rollout tracker (memory)

---

## Quick command sequence (copy-paste for a new run)

### Mode A: Full-page

```bash
# 1. Set up project dir
mkdir -p /workspace/<route>-redesign && cd /workspace/<route>-redesign

# 2. (Build index.html — see prompt template above)

# 3. Validate
python3 validate.py   # see validate.py template in the SKILL examples

# 4. Zip (single file, no cruft)
cd /workspace && zip -qr <route>-redesign-source.zip <route>-redesign/index.html

# 5. Deploy
website_deploy --path=/workspace/<route>-redesign --project_name="<route> — design system v1"

# 6. Commit
cd /workspace/<route>-redesign
git init 2>/dev/null  # no-op if already a repo
git add -A
git commit -m "redesign: <route> via apply-design-system skill

- Source: <source URL or file>
- Reference: <reference file>
- Sections: <count> preserved, <count> restyled
- Functionality: <count> handlers preserved
- Validation: light ✓ dark ✓"

# 7. Cleanup old artifacts (if this is a v2+)
rm -rf /workspace/<route>-redesign-v1 2>/dev/null
rm -f /workspace/<route>-redesign-v1-source.zip 2>/dev/null
mavis drive files delete --node_id=<old_preview_node_id>
```

### Mode B: Section-by-section

```bash
# 1. Copy the current index.html into a project dir
mkdir -p /workspace/<route>-section-update
cp <current-deployed>/index.html /workspace/<route>-section-update/index.html

# 2. (Edit just the target section in the new index.html — see section-by-section workflow)

# 3. Diff to confirm only the target section changed
diff <current-deployed>/index.html /workspace/<route>-section-update/index.html

# 4. Validate
cd /workspace/<route>-section-update
python3 validate.py

# 5. Commit
git init 2>/dev/null
git add -A
git commit -m "section-update: <route> · <section name>

- Section: <class or id>
- Change: <visual only | component swap | new sub-component>
- Other sections: byte-identical to HEAD
- Validation: light ✓ dark ✓"

# 6. Deploy preview (optional)
website_deploy --path=/workspace/<route>-section-update --project_name="<route> — <section> update"
```

### Commit-only (no change)

```bash
# Just commit the current state (e.g., after a manual fix)
cd /workspace/<project>
git add -A
git commit -m "fix: <description>"
```

---

## When the skill is wrong for the job

- The user wants a fresh page with no source to preserve → use `landing-page-builder`
- The user wants a real component library (React/Vue/Svelte) → not this skill; the output here is a static single HTML
- The user wants the design system itself extracted from a page → not this skill; ask for the reference first
- The user wants to change content or add a new section → not this skill; the constraint "without changing sections/content" is binding

---

## Patterns for real-world pages (learned from actual runs)

This section is updated after each redesign run with patterns that came up in practice. Treat it as a checklist of things the prompt template doesn't explicitly call out but you'll hit.

### Large existing pages: use a transform, don't rewrite

For a source page with 1500+ lines and lots of existing behavior, do **not** rewrite from scratch. The risk of dropping a functionality handler is too high. Instead:

1. Read the source file
2. Use a script to:
   - Strip all `<style>...</style>` blocks (per the app-level cleanup rule)
   - Strip `<link rel="stylesheet" href="...">` to old stylesheets (keep only Google Fonts)
   - Strip inline `style="..."` attributes that are pure styling (keep ones that JS sets dynamically)
   - Inject the design system CSS at the top of `<head>`
   - Inject site-specific component CSS that the design system doesn't cover (e.g., nav dropdowns, mobile nav, header layout)
   - Keep all `<body>` DOM, all `<script>` blocks, all IDs, all event handlers, all JSON-LD, all `<meta>`, all `<link rel="preconnect">`
3. Save as the new `index.html`

This keeps the diff small and the functionality intact. The output is a clean reimplementation that happens to have the same content as the source.

### External scripts (site-shell.js, api-data.js, cookie-consent.js)

Production pages often load their own JS files for things like theme switching, mobile nav, and cookie consent. These files:
- Are loaded as `<script src="./home_files/...">` in the source
- Use class names like `[data-theme-btn]`, `.nav-toggle`, etc.
- Are NOT in the design system reference

**Preserve the `<script>` tags in the output.** When the user deploys to their Worker, these files live in the same directory and resolve. When testing locally, these 404 — that's expected and not a real failure (filter them out of the validation).

### localStorage theme key may differ from the design system reference

The design system reference uses `dt-theme` as the theme localStorage key. The source page may use a different key (e.g., `tdp-theme`, `theme-pref`, `theme`, etc.).

**Inventory the actual key** by reading the source's site-shell.js (or any inline JS that reads/writes theme). Use the source's key, not the design system's. The output must call `localStorage.setItem('SAME_KEY', 'dark')` and `getItem('SAME_KEY')` to keep theme persistence working.

### Initial theme should match the source page's default

The design system reference may default to dark mode. The source page may default to light. **Keep the source's default** — don't override `<html data-theme="...">` to match the design system. The site-shell.js will update the attribute on load based on saved preference / system preference.

### Components that depend on the OLD CSS need explicit re-styles

After stripping the old `<style>` blocks, any component that was styled by them will lose its layout. You typically need to re-add CSS for:
- **Header layout** — `.header-row`, `.logo`, `.logo-mark`, `.logo-text`, `.nav-main`, `.nav-link`, `.header-actions`
- **Nav dropdowns** — `.nav-dropdown`, `.nav-item.has-dropdown:hover .nav-dropdown`, `.dropdown-item`, `.dropdown-divider`, `.dropdown-section-label`, `.dropdown-arrow`
- **Mobile nav** — `.mobile-nav`, `.mobile-nav-backdrop`, `.mobile-nav-toggle`
- **Page-specific components** — pills, rail cards, search, snapshot grid, lwf, person grids, faq, continue strip, feedback widget, cookie banner

The design system provides the **tokens** (colors, type, spacing). You write the **component CSS** that uses those tokens, on top of the design system.

### Mobile nav and dropdowns must be hidden by default

The source's CSS likely had `.mobile-nav { display: none }` and `.nav-dropdown { display: none }` that I stripped. Without them, the mobile nav and dropdowns are always visible, overlapping the header.

**Always add:**
```css
.mobile-nav[hidden] { display: none !important; }
.nav-dropdown { display: none; position: absolute; ... }
.nav-item.has-dropdown:hover .nav-dropdown,
.nav-item.has-dropdown:focus-within .nav-dropdown { display: block; }
```

### When the page has 15+ sections, don't try to enforce scroll-reveal on all of them

The scroll-reveal pattern (add `data-reveal` to each section element, fade in on viewport entry) is a nice touch but breaks down on dense pages with 15+ content sections — too much is animating at once and the effect becomes noise.

For dense pages:
- Apply `data-reveal` to the major top-level sections (hero, clock, favorites, etc.)
- Skip the inner grids/lists — let them appear with the section
- Or skip scroll-reveal entirely if the page is too dense

### API base URL switcher

Production pages often have:
```js
const API = (function () {
  const h = location.hostname;
  if (h === "dateandtime.live" || h.endsWith(".dateandtime.live")) return "https://api.dateandtime.live";
  if (h.endsWith(".workers.dev")) return "https://dev.api.dateandtime.live";
  return "";  // same-origin
})();
```

**Don't change this.** The Worker has its own API proxy. When the user deploys to `dateandtime.live`, it hits prod. When deployed to `tdp-landing-dev.*.workers.dev`, it hits dev. Local file:// uses same-origin (which fails in local testing — that's expected).

### Validating locally

Local validation has known limitations:
- External scripts 404 (expected, filter them)
- API calls fail (file:// can't reach HTTPS APIs, expected)
- The theme toggle may not work because site-shell.js doesn't load locally
- Mobile nav may stay open because the JS that closes it doesn't load

**Approach:** validate that the design system CSS works by manually setting `data-theme` via `page.evaluate()`. Validate that the DOM structure is correct. Validate that no internal 404s (images, inlined SVGs) occur. Accept that JS-driven behavior needs the production server to verify.

```python
await page.goto(f"file://{INDEX}", wait_until="domcontentloaded", timeout=30000)
# Force the data-theme (the missing site-shell.js would normally do this)
await page.evaluate(f"document.documentElement.setAttribute('data-theme', '{theme}')")
await page.wait_for_timeout(500)
```

### Component CSS goes in a `<style id="site-overrides">` block

Put page-specific component CSS (header, nav, pills, rail, etc.) in a separate `<style>` block after the design system block. Comment it clearly so future runs know what's design-system vs. site-specific.

### Refactor opportunity: extract the transform into a reusable script

After the second or third time you run this skill on a similar production page, the transform script (read source → strip CSS → inject design system → save) is reusable. Save it to the project dir as `build.py` and reuse it across runs. The only thing that changes between runs is:
- The design system reference file (may evolve)
- The site-overrides CSS (component CSS that the design system doesn't cover)
- The localStorage key inventory (may differ per page)
- The expected 404 filter (which external scripts are present)
