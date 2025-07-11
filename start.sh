#!/bin/bash

# Install Playwright Chromium (needed for scraping)
python -m playwright install chromium

# Start the Flask app using Gunicorn
gunicorn app:app --bind 0.0.0.0:8080
