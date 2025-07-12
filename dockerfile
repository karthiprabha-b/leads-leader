# Use lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright Chromium
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 \
    libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-0 libx11-6 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
    libgbm1 libxcb1 libxkbcommon0 libpango-1.0-0 libcairo2 \
    libasound2 wget curl unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy everything
COPY . .

# Install Python deps
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright browser
RUN playwright install chromium

# Make start.sh executable
RUN chmod +x scripts/start.sh

# Set entrypoint
CMD ["bash", "scripts/start.sh"]
