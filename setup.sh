#!/bin/bash

# Update system
apt-get update
apt-get upgrade -y

# Install Python and pip
apt-get install -y python3 python3-pip

# Install Chrome and ChromeDriver
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
apt-get update
apt-get install -y google-chrome-stable

# Install ChromeDriver
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1)
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}
CHROMEDRIVER_VERSION=$(cat LATEST_RELEASE_${CHROME_VERSION})
wget https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Create bot directory
mkdir -p /opt/chatbots
cd /opt/chatbots

# Copy bot files
cp /tmp/chatbots/* /opt/chatbots/

# Install Python dependencies
pip3 install -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/chatbots.service << EOL
[Unit]
Description=ChatSafari Bots Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/chatbots
ExecStart=/usr/bin/python3 chat_bots.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Start service
systemctl daemon-reload
systemctl enable chatbots
systemctl start chatbots

# Clean up
rm -rf /tmp/chatbots 