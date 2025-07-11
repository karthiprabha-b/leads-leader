from flask import Flask, render_template, request, jsonify, session, send_file
import openai
import io
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Scraper imports
from services.google_maps_service import search_google_places
from services.justdial_scraper import scrape_justdial
from services.linkedin_scraper import scrape_linkedin
from services.instagram_scraper import scrape_instagram
from services.facebook_scraper import scrape_facebook

app = Flask(__name__)
app.secret_key = "xtractlead-secret"

@app.route("/", methods=["GET", "POST"])
def index():
    leads = []
    if request.method == "POST":
        niche = request.form.get("niche")
        location = request.form.get("location")
        platform = request.form.get("platform")

        if not niche or not location or not platform:
            return render_template("index.html", leads=[])

        if platform == "googlemaps":
            leads = search_google_places(niche, location)
        elif platform == "justdial":
            leads = scrape_justdial(niche, location)
        elif platform == "linkedin":
            leads = scrape_linkedin(niche, location)
        elif platform == "instagram":
            leads = scrape_instagram(niche, location)
        elif platform == "facebook":
            leads = scrape_facebook(niche, location)

        session["leads"] = leads

    else:
        leads = session.get("leads", [])

    return render_template("index.html", leads=leads)

@app.route("/mark-contacted", methods=["POST"])
def mark_contacted():
    data = request.json
    name = data.get("name")
    leads = session.get("leads", [])
    for lead in leads:
        if lead["name"] == name:
            lead["contacted"] = True
    session["leads"] = leads
    return jsonify({"status": "updated"})

@app.route("/export-csv")
def export_csv():
    leads = session.get("leads", [])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Address", "Phone", "Email", "Contacted", "Source"])
    for lead in leads:
        writer.writerow([
            lead.get("name", ""),
            lead.get("address", ""),
            lead.get("phone", ""),
            lead.get("email", ""),
            lead.get("contacted", False),
            lead.get("source", "")
        ])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype="text/csv", as_attachment=True, download_name="leads.csv")

@app.route("/generate-message", methods=["POST"])
def generate_message():
    data = request.json
    business_type = data.get("business_type")
    lead_name = data.get("lead_name")

    prompt = f"Write a professional and friendly WhatsApp message introducing a {business_type} business to {lead_name}. Keep it short, clear, and engaging."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7
        )
        message = response.choices[0].message.content.strip()
        return jsonify({"message": message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
