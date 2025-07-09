from flask import Flask, render_template, request, jsonify, session, send_file
import requests
import openai
import io
import csv

app = Flask(__name__)
app.secret_key = "leads-leader-key"  # Needed for session tracking

# API Keys
SERPAPI_KEY = "d34214eacdd41a1b27827435b115426a3aacfa051f4e776ff982e08a1b4a5cb4"
OPENAI_API_KEY = "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"
PHANTOMBUSTER_API_KEY = "mnrosaWWZB1gRUdozrmz81ox7HLUqLT5E73O5V150CU"

openai.api_key = OPENAI_API_KEY

# Leads fetching (only Google for now)
def get_google_maps_leads(niche, location):
    query = f"{niche} in {location}"
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_maps",
        "q": query,
        "type": "search",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    if "local_results" in data:
        for item in data["local_results"]:
            name = item.get("title", "")
            address = item.get("address", "")
            phone = item.get("phone", "")
            results.append({
                "name": name,
                "address": address,
                "phone": phone.replace(" ", "").replace("+", "") if phone else "",
                "contacted": False
            })
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    leads = []
    if request.method == "POST":
        niche = request.form.get("niche")
        location = request.form.get("location")
        platform = request.form.get("platform")
        status_filter = request.form.get("status")

        if platform == "googlemaps":
            leads = get_google_maps_leads(niche, location)

        # Save to session
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
    writer.writerow(["Name", "Address", "Phone", "Contacted"])
    for lead in leads:
        writer.writerow([lead["name"], lead["address"], lead["phone"], lead.get("contacted", False)])
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
    app.run(host="0.0.0.0", port=8080)
