FROM python:3.9-slim

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    curl \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable=114.0.5735.90-1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_VERSION="114.0.5735.90" \
    && CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) \
    && echo "Installing ChromeDriver for Chrome $CHROME_MAJOR_VERSION" \
    && CHROMEDRIVER_VERSION="114.0.5735.90" \
    && curl -s -o chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" \
    && unzip chromedriver.zip -d /usr/local/bin/ \
    && rm chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver

# Set up working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV CHROME_DRIVER_PATH=/usr/local/bin/chromedriver

# Start Xvfb and run the bot
CMD Xvfb :99 -screen 0 1280x1024x24 > /dev/null 2>&1 & python run_bots.py
