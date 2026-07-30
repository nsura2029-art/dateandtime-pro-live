"""Take a screenshot of the deployed hero for preview."""
import time
from playwright.sync_api import sync_playwright

URL = "https://29jsuafnz412v.space.minimax.io/"

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=20000)
    time.sleep(2)

    # Light mode
    page.screenshot(path="/workspace/dateandtime-pro-live/imgs/_preview-light.png",
                    clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    print("Light: imgs/_preview-light.png")

    # Dark mode
    page.evaluate("""
        () => {
            localStorage.setItem('tdp-theme', 'dark');
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    """)
    time.sleep(1)
    page.screenshot(path="/workspace/dateandtime-pro-live/imgs/_preview-dark.png",
                    clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    print("Dark: imgs/_preview-dark.png")

    # Mobile preview
    ctx_m = browser.new_context(viewport={"width": 390, "height": 844},
                                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)")
    page_m = ctx_m.new_page()
    page_m.goto(URL, wait_until="networkidle", timeout=20000)
    time.sleep(2)
    page_m.screenshot(path="/workspace/dateandtime-pro-live/imgs/_preview-mobile.png",
                      full_page=False)
    print("Mobile: imgs/_preview-mobile.png")

    # Read what's actually rendered
    time_text = page.locator("#hero-current-time").text_content()
    city = page.locator("#hero-current-city").text_content()
    region = page.locator("#hero-current-region").text_content()
    print(f"\nLive data: {time_text} · {city} · {region}")

    browser.close()
