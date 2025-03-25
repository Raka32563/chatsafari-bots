import os
import sys
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='deploy.log'
)

class CloudDeployer:
    def __init__(self, provider='aws'):
        self.provider = provider
        self.instance_type = 't2.micro'  # Smallest instance type
        self.region = 'us-east-1'  # Default region
        self.image_id = None
        self.instance_id = None
        
    def setup_aws(self):
        """Setup AWS EC2 instance"""
        try:
            # Install AWS CLI if not present
            subprocess.run(['aws', '--version'], check=True)
        except subprocess.CalledProcessError:
            logging.info("Installing AWS CLI...")
            subprocess.run(['pip', 'install', 'awscli'])
            
        # Configure AWS credentials
        if not os.path.exists(os.path.expanduser('~/.aws/credentials')):
            logging.info("Please configure AWS credentials using 'aws configure'")
            return False
            
        return True
        
    def create_instance(self):
        """Create a new EC2 instance"""
        try:
            # Create security group
            sg_name = f"chatbots-sg-{datetime.now().strftime('%Y%m%d')}"
            subprocess.run([
                'aws', 'ec2', 'create-security-group',
                '--group-name', sg_name,
                '--description', 'Security group for ChatSafari bots'
            ])
            
            # Allow necessary ports
            subprocess.run([
                'aws', 'ec2', 'authorize-security-group-ingress',
                '--group-name', sg_name,
                '--protocol', 'tcp',
                '--port', '22',
                '--cidr', '0.0.0.0/0'
            ])
            
            # Launch instance
            response = subprocess.run([
                'aws', 'ec2', 'run-instances',
                '--image-id', 'ami-0c7217cdde317cfec',  # Ubuntu 22.04 LTS
                '--instance-type', self.instance_type,
                '--security-groups', sg_name,
                '--key-name', 'chatbots-key',
                '--user-data', 'file://setup.sh'
            ], capture_output=True, text=True)
            
            # Parse instance ID from response
            self.instance_id = response.stdout.split('"InstanceId": "')[1].split('"')[0]
            logging.info(f"Created instance {self.instance_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to create instance: {str(e)}")
            return False
            
    def setup_instance(self):
        """Setup the instance with required software"""
        try:
            # Create setup script
            setup_script = """#!/bin/bash
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
# (You'll need to implement file transfer)

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

[Install]
WantedBy=multi-user.target
EOL

# Start service
systemctl daemon-reload
systemctl enable chatbots
systemctl start chatbots
"""
            
            with open('setup.sh', 'w') as f:
                f.write(setup_script)
                
            return True
            
        except Exception as e:
            logging.error(f"Failed to create setup script: {str(e)}")
            return False
            
    def deploy(self):
        """Deploy the bot system to cloud"""
        if self.provider == 'aws':
            if not self.setup_aws():
                return False
                
            if not self.setup_instance():
                return False
                
            if not self.create_instance():
                return False
                
            logging.info("Deployment completed successfully")
            return True
            
        else:
            logging.error(f"Unsupported provider: {self.provider}")
            return False

if __name__ == "__main__":
    deployer = CloudDeployer()
    if deployer.deploy():
        print("Deployment successful!")
    else:
        print("Deployment failed. Check deploy.log for details.") 