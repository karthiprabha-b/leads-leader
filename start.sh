#!/bin/bash
# Install browsers before running the app
python3 -m playwright install chromium

# Then run gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT
