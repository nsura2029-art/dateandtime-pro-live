"""Quick hero validation — check that the redesigned hero renders and the time updates."""
import sys
import time
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/index.html"
errors = []
warnings = []

def main():
    with sync_playwright() as p:
        for scheme in ("light", "dark"):
            print(f"\n=== {scheme.upper()} MODE ===")
            browser = p.chromium.launch()
            ctx = browser.new_context(color_scheme=scheme, viewport={"width": 1440, "height": 900})
            page = ctx.new_page()

            page_errors = []
            page.on("pageerror", lambda e: page_errors.append(str(e)))
            console_errors = []
            page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)

            page.goto(URL, wait_until="networkidle", timeout=15000)
            time.sleep(2)  # let JS update

            # Check page-level theme
            theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
            print(f"  data-theme = {theme}")

            # Check hero section
            hero_visible = page.locator(".section--hero").is_visible()
            print(f"  hero visible = {hero_visible}")
            if not hero_visible:
                errors.append(f"{scheme}: hero not visible")

            # Check the time element exists and is visible
            time_text = page.locator("#hero-current-time").text_content()
            time_visible = page.locator("#hero-current-time").is_visible()
            print(f"  hero time = '{time_text}' (visible={time_visible})")
            if not time_text or not any(c.isdigit() for c in time_text):
                errors.append(f"{scheme}: hero time is empty or has no digits")
            if not time_visible:
                errors.append(f"{scheme}: hero time not visible")

            # Check the time actually updates
            time1 = time_text
            time.sleep(1.5)
            time2 = page.locator("#hero-current-time").text_content()
            if time1 == time2:
                warnings.append(f"{scheme}: time did not change in 1.5s — may be stuck")
            else:
                print(f"  time changed: '{time1}' → '{time2}' ✓")

            # Check city / region / tz
            city = page.locator("#hero-current-city").text_content()
            region = page.locator("#hero-current-region").text_content()
            tz_abbr = page.locator("#tz-abbr").text_content()
            print(f"  city='{city}' region='{region}' tz='{tz_abbr}'")

            # Check the city has actual text
            if not city or len(city) < 2:
                errors.append(f"{scheme}: city text empty or too short")

            # Check the hero time font-size is BIG (the redesign's whole point)
            time_font_size = page.evaluate("""
                () => {
                    const el = document.getElementById('hero-current-time');
                    return parseFloat(getComputedStyle(el).fontSize);
                }
            """)
            print(f"  hero time font-size = {time_font_size}px")
            if time_font_size < 40:
                errors.append(f"{scheme}: hero time font-size {time_font_size}px is too small (visual focal point must be ≥40px)")

            # Check the format toggle works (12h ↔ 24h)
            format_12_pressed = page.locator("#format-12").get_attribute("aria-pressed")
            print(f"  12h button aria-pressed = {format_12_pressed}")

            # Take a screenshot for visual inspection
            page.screenshot(path=f"/workspace/dateandtime-pro-live/imgs/_hero-{scheme}.png", full_page=False, clip={"x": 0, "y": 0, "width": 1440, "height": 900})
            print(f"  screenshot: imgs/_hero-{scheme}.png")

            if page_errors:
                errors.extend([f"{scheme}: page error: {e}" for e in page_errors])
            if console_errors:
                warnings.extend([f"{scheme}: console error: {e}" for e in console_errors])

            browser.close()

    print("\n=== SUMMARY ===")
    if warnings:
        print(f"  {len(warnings)} warning(s):")
        for w in warnings:
            print(f"    - {w}")
    if errors:
        print(f"  {len(errors)} error(s):")
        for e in errors:
            print(f"    - {e}")
        sys.exit(1)
    else:
        print("  All checks passed ✓")

if __name__ == "__main__":
    main()
