#!/bin/bash
# Make sure Playwright dependencies are installed
playwright install chromium

# Start Gunicorn server
exec gunicorn -b 0.0.0.0:8080 app:app
