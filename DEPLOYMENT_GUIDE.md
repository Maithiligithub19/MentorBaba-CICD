# QuizXMentor CI/CD Pipeline Setup Guide

## Overview
This guide covers the complete setup of CI/CD pipeline for QuizXMentor Flask application using Jenkins, Docker, and AWS EC2.

## Prerequisites
- AWS Account with EC2 access
- GitHub repository
- Domain/Email for notifications

## 1. AWS EC2 Setup

### Launch EC2 Instance
```bash
# Instance Type: t2.medium or higher
# AMI: Ubuntu 20.04 LTS
# Security Group: Allow ports 22, 5000, 8080
# Key Pair: Create and download .pem file
```

### Configure EC2
```bash
# SSH to EC2 instance
ssh -i your-key.pem ubuntu@43.204.141.56

# Run setup script
chmod +x aws-setup.sh
./aws-setup.sh
```

## 2. Jenkins Configuration

### Initial Setup
```bash
# Get Jenkins initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

# Access Jenkins at http://43.204.141.56:8080
# Install suggested plugins
# Create admin user
```

### Install Required Plugins
- Docker Pipeline
- Email Extension Plugin
- GitHub Integration Plugin
- Pipeline Plugin

### Configure Email Notifications
```
Manage Jenkins → Configure System → Extended E-mail Notification
SMTP Server: smtp.gmail.com
SMTP Port: 587
Username: your-email@gmail.com
Password: your-app-password
```

## 3. GitHub Webhook Setup

### Repository Settings
```
GitHub Repository → Settings → Webhooks → Add webhook
Payload URL: http://43.204.141.56:8080/github-webhook/
Content type: application/json
Events: Push events
```

## 4. Jenkins Pipeline Setup

### Create New Pipeline Job
```
New Item → Pipeline → Enter name "QuizXMentor-Pipeline"
Pipeline → Definition: Pipeline script from SCM
SCM: Git
Repository URL: https://github.com/Maithiligithub19/MentorBaba-CICD.git
Branch: main
Script Path: Jenkinsfile
```

### Environment Variables
```
Pipeline → Environment Variables:
IMAGE_NAME = quizxmentor
CONTAINER_NAME = quizapp
PORT = 5000
EMAIL = maithilisude19@gmail.com
```

## 5. Application Configuration

### Environment File
```bash
# Copy .env.example to .env and configure
cp .env.example .env

# Edit .env with your database credentials
DB_HOST=localhost
DB_USER=quizapp
DB_PASSWORD=password123
DB_NAME=quiz_app2
```

### Database Setup
```bash
# Install MySQL on EC2
sudo apt-get install -y mysql-server

# Create database and user
mysql -u root -p
CREATE DATABASE quiz_app2;
CREATE USER 'quizapp'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON quiz_app2.* TO 'quizapp'@'localhost';
FLUSH PRIVILEGES;

# Import schema
mysql -u quizapp -p quiz_app2 < corrected_schema.sql
```

## 6. Pipeline Stages Explained

### Stage 1: Clone Repository
- Pulls latest code from GitHub main branch
- Triggered by webhook on code push

### Stage 2: Build Docker Image
- Creates Docker image using Dockerfile
- Tags image as 'quizxmentor'

### Stage 3: Stop Previous Container
- Stops running container gracefully
- Removes old container to free resources

### Stage 4: Run New Container
- Starts new container with updated code
- Maps port 5000 for web access
- Uses environment file for configuration

### Stage 5: Email Notification
- Sends deployment success email
- Includes application URL
- Notifies team of deployment status

## 7. Deployment Commands

### Manual Deployment
```bash
# Make deployment script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Pipeline Trigger
```bash
# Push code to trigger pipeline
git add .
git commit -m "Deploy to production"
git push origin main
```

## 8. Monitoring & Troubleshooting

### Check Application Status
```bash
# Check container status
docker ps

# View application logs
docker logs quizapp

# Check application health
curl http://43.204.141.56:5000/api/health
```

### Jenkins Logs
```bash
# View Jenkins logs
sudo journalctl -u jenkins -f

# Check pipeline console output in Jenkins UI
```

### Common Issues
1. **Port conflicts**: Ensure port 5000 is available
2. **Database connection**: Verify MySQL is running and credentials are correct
3. **Email notifications**: Check SMTP settings and app passwords
4. **Webhook failures**: Verify GitHub webhook URL and Jenkins accessibility

## 9. Security Considerations

### EC2 Security
- Use security groups to restrict access
- Keep system updated
- Use IAM roles instead of access keys
- Enable CloudTrail for auditing

### Application Security
- Use environment variables for secrets
- Enable HTTPS in production
- Implement proper authentication
- Regular security updates

## 10. Scaling & Optimization

### Performance
- Use load balancer for multiple instances
- Implement database connection pooling
- Add Redis for session management
- Use CDN for static assets

### Monitoring
- Set up CloudWatch for metrics
- Implement application logging
- Use health checks
- Monitor resource usage

## Application URLs
- **Production**: http://43.204.141.56:5000
- **Jenkins**: http://43.204.141.56:8080
- **Health Check**: http://43.204.141.56:5000/api/health

## Support
For issues or questions, contact: maithilisude19@gmail.com