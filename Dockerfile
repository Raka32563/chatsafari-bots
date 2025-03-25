FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    unzip \
    xvfb \
    ca-certificates \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    libappindicator3-1 \
    libdbusmenu-glib4 \
    libdbusmenu-gtk3-4 \
    libgbm1 \
    libgtk-3-0 \
    libpango1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Verify Google Chrome Installation
RUN google-chrome --version || echo "Google Chrome failed to install"

# Install ChromeDriver (Matching Stable Chrome)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') \
    && CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) \
    && echo "Installing ChromeDriver for Chrome $CHROME_MAJOR_VERSION" \
    && CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION") \
    && [ -n "$CHROMEDRIVER_VERSION" ] || (echo "Failed to fetch ChromeDriver version!" && exit 1) \
    && curl -s -o chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver.zip -d /usr/local/bin \
    && rm chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Verify ChromeDriver Installation
RUN chromedriver --version || echo "ChromeDriver failed to install"

# Set up working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Start Xvfb and run the bot
CMD Xvfb :99 -screen 0 1280x1024x24 > /dev/null 2>&1 & python run_bots.py
