# ChatSafari Bot System

This system creates automated bots to simulate users on ChatSafari.com.

## Directory Structure
```
Chatbots/
├── chat_bots.py      # Main bot implementation
├── deploy.py         # Cloud deployment script
├── requirements.txt  # Python dependencies
├── setup.sh         # Server setup script
└── README.md        # This file
```

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- AWS account (for cloud deployment)
- AWS CLI installed and configured

## Local Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Chrome WebDriver:
   - Download ChromeDriver from https://sites.google.com/chromium.org/driver/
   - Add ChromeDriver to your system PATH

3. Run the bots locally:
```bash
python chat_bots.py
```

## Cloud Deployment

1. Configure AWS credentials:
```bash
aws configure
```

2. Create SSH key pair:
```bash
aws ec2 create-key-pair --key-name chatbots-key --query 'KeyMaterial' --output text > chatbots-key.pem
chmod 400 chatbots-key.pem
```

3. Deploy to AWS:
```bash
python deploy.py
```

## Monitoring

- Check logs: `chat_bots.log`
- Monitor AWS EC2 instance through AWS Console
- SSH into instance: `ssh -i chatbots-key.pem ubuntu@<instance-ip>`

## Important Notes

- Bots run in headless mode
- Each bot has random age between 16-32
- System includes automatic error recovery
- Service restarts automatically on failure
- Monitor AWS costs regularly

## Security

- Keep AWS credentials secure
- Don't share SSH keys
- Monitor instance security
- Regular security updates

## Maintenance

- Update ChromeDriver when Chrome updates
- Monitor bot responses
- Check logs for issues
- Regular AWS cost review 