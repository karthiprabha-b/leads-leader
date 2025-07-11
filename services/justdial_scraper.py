from playwright.sync_api import sync_playwright
import re

def extract_email(text):
    match = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return match[0] if match else None

def scrape_justdial(niche, location, max_results=10):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        search_url = f"https://www.justdial.com/{location}/{niche}"
        page.goto(search_url, timeout=60000)
        page.wait_for_selector(".cntanr", timeout=10000)

        containers = page.query_selector_all(".cntanr")
        leads = []

        for container in containers[:max_results]:
            name = container.query_selector(".lng_cont_name")
            phone = container.query_selector(".contact-info span")
            address = container.query_selector(".cont_sw_addr")
            link = container.query_selector("a")

            name = name.inner_text().strip() if name else ""
            phone = phone.inner_text().strip() if phone else ""
            address = address.inner_text().strip() if address else ""
            href = link.get_attribute("href") if link else None

            email = None
            if href:
                detail = browser.new_page()
                try:
                    detail.goto(href, timeout=60000)
                    body_text = detail.inner_text("body")
                    email = extract_email(body_text)
                except:
                    pass
                detail.close()

            leads.append({
                "name": name,
                "address": address,
                "phone": phone,
                "email": email,
                "contacted": False
            })

        browser.close()
        return leads
