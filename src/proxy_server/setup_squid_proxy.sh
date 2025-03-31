#!/bin/bash

# Install Squid
echo "Installing Squid..."
if command -v apt >/dev/null; then
  sudo apt update && sudo apt install squid apache2-utils -y
elif command -v yum >/dev/null; then
  sudo yum update -y && sudo yum install squid httpd-tools -y
else
  echo "Unsupported OS. Please use Ubuntu or Amazon Linux."
  exit 1
fi

# Backup original config
sudo cp /etc/squid/squid.conf /etc/squid/squid.conf.bak

# Create password file
read -p "Enter username for proxy auth: " proxy_user
sudo touch /etc/squid/passwd
sudo chown squid /etc/squid/passwd
sudo htpasswd -b /etc/squid/passwd $proxy_user "$(openssl rand -base64 12)"

# Replace config
cat <<EOF | sudo tee /etc/squid/squid.conf > /dev/null
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic realm proxy
acl authenticated proxy_auth REQUIRED

http_access allow authenticated
http_port 3128
EOF

# Enable firewall access (optional – depends on your OS/firewall setup)
echo "Make sure port 3128 is open in your EC2 Security Group."

# Restart Squid
echo "Restarting Squid..."
sudo systemctl restart squid
sudo systemctl enable squid

# Get EC2 instance public IP
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "✅ Proxy setup complete!"
echo "Use: http://$EC2_IP:3128 with username: $proxy_user"
