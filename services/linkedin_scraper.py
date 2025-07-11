from playwright.sync_api import sync_playwright
import re

def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match[0] if match else None

def scrape_linkedin(niche, location, max_results=5):
    leads = []
    with sync_playwright() as p:
        # ✅ Add --no-sandbox for Railway compatibility
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()

        query = f"{niche} in {location} site:linkedin.com"
        page.goto(f"https://www.google.com/search?q={query}", timeout=60000)
        page.wait_for_selector("a")
        links = page.query_selector_all("a")

        for link in links[:max_results]:
            href = link.get_attribute("href")
            if href and ("linkedin.com/in/" in href or "linkedin.com/company/" in href):
                detail = browser.new_page()
                try:
                    detail.goto(href, timeout=60000)
                    body = detail.inner_text("body")
                    email = extract_email(body)
                    title = detail.title().split("|")[0].strip()
                    leads.append({
                        "name": title,
                        "email": email,
                        "source": href,
                        "contacted": False
                    })
                except:
                    pass
                detail.close()

        browser.close()
    return leads