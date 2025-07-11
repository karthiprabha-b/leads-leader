#!/bin/bash

echo "Installing Playwright Chromium..."
python -m playwright install chromium

echo "Starting Gunicorn server..."
gunicorn app:app --bind 0.0.0.0:8000
