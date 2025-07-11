# Use slim Python base image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies needed for Playwright Chromium
RUN apt-get update && apt-get install -y \
    wget curl gnupg2 ca-certificates fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 \
    libnspr4 libnss3 libx11-6 libxcomposite1 libxdamage1 libxext6 \
    libxfixes3 libxrandr2 libxcb1 libxkbcommon0 libpango-1.0-0 \
    libcairo2 libatspi2.0-0 --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright Chromium and dependencies
RUN playwright install --with-deps

# Copy project files
COPY . .

# Expose app port
EXPOSE 8080

# Start Flask app via gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
