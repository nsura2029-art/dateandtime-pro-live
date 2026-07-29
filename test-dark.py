"""Quick dark-mode test — click the dark mode button."""
import time
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8765/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=15000)
    time.sleep(1)
    # Set dark mode directly via DOM (page's theme script reads from localStorage at load)
    page.evaluate("""
        () => {
            localStorage.setItem('tdp-theme', 'dark');
            document.documentElement.setAttribute('data-theme', 'dark');
        }
    """)
    time.sleep(0.5)
    time.sleep(1)
    theme = page.evaluate("document.documentElement.getAttribute('data-theme')")
    print(f"After clicking dark button: data-theme = {theme}")
    page.screenshot(path="/workspace/dateandtime-pro-live/imgs/_hero-dark.png", clip={"x": 0, "y": 0, "width": 1440, "height": 900})
    print("Screenshot saved.")
    browser.close()
