#!/bin/bash
python -m playwright install chromium
gunicorn app:app --bind 0.0.0.0:8080
