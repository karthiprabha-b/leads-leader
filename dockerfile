# Use official Playwright image with all dependencies pre-installed
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright with required browser dependencies
RUN playwright install --with-deps

# Expose the port your app runs on
EXPOSE 8080

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
