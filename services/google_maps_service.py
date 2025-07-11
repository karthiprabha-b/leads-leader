# services/google_maps_service.py

import requests
import os
import re
from bs4 import BeautifulSoup

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def extract_email_from_website(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(email_regex, soup.get_text())
        return emails[0] if emails else None
    except:
        return None

def search_google_places(niche, location, max_results=15):
    search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "query": f"{niche} in {location}",
        "key": GOOGLE_API_KEY
    }

    leads = []
    response = requests.get(search_url, params=params).json()
    results = response.get("results", [])

    for place in results[:max_results]:
        place_id = place.get("place_id")
        details_params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,website",
            "key": GOOGLE_API_KEY
        }

        details_res = requests.get(details_url, params=details_params).json()
        detail = details_res.get("result", {})

        email = extract_email_from_website(detail.get("website")) if detail.get("website") else None

        leads.append({
            "name": detail.get("name", ""),
            "address": detail.get("formatted_address", ""),
            "phone": detail.get("formatted_phone_number", ""),
            "email": email,
            "contacted": False
        })

    return leads
 