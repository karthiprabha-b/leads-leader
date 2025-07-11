from playwright.sync_api import sync_playwright
import re

def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match[0] if match else None

def scrape_facebook(niche, location, max_results=5):
    leads = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        search_query = f"{niche} {location} site:facebook.com"
        page.goto(f"https://www.google.com/search?q={search_query}", timeout=60000)
        page.wait_for_selector("a")
        links = page.query_selector_all("a")

        for link in links[:max_results]:
            href = link.get_attribute("href")
            if href and "facebook.com" in href:
                detail = browser.new_page()
                try:
                    detail.goto(href, timeout=60000)
                    body = detail.inner_text("body")
                    email = extract_email(body)
                    name = href.split("/")[-2]
                    leads.append({
                        "name": name,
                        "email": email,
                        "source": href,
                        "contacted": False
                    })
                except:
                    pass
                detail.close()

        browser.close()
    return leads
