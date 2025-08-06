#!/bin/bash

# AWS EC2 Setup Script for QuizXMentor
# Run this script on your EC2 instance

set -e

echo "Setting up EC2 instance for QuizXMentor deployment..."

# Update system
sudo apt-get update -y

# Install Docker
echo "Installing Docker..."
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install MySQL client
echo "Installing MySQL client..."
sudo apt-get install -y mysql-client

# Install Jenkins (if not already installed)
echo "Installing Jenkins..."
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update -y
sudo apt-get install -y openjdk-11-jdk jenkins

# Start services
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Configure firewall
echo "Configuring firewall..."
sudo ufw allow 22
sudo ufw allow 5000
sudo ufw allow 8080
sudo ufw --force enable

echo "EC2 setup completed!"
echo "Jenkins is available at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
echo "Initial Jenkins password: sudo cat /var/lib/jenkins/secrets/initialAdminPassword"