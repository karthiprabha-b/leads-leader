#!/bin/bash
playwright install --with-deps
gunicorn -b 0.0.0.0:8080 app:app
