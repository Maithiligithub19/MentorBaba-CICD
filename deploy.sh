#!/bin/bash

# AWS Deployment Script for QuizXMentor
# Usage: ./deploy.sh

set -e

# Configuration
IMAGE_NAME="quizxmentor"
CONTAINER_NAME="quizapp"
PORT="5000"
EC2_HOST="43.204.141.56"
EC2_USER="ubuntu"
KEY_PATH="~/.ssh/aws-key.pem"

echo "Starting deployment to AWS EC2..."

# Build Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Save image to tar file
echo "Saving Docker image..."
docker save $IMAGE_NAME > quizxmentor.tar

# Copy files to EC2
echo "Copying files to EC2..."
scp -i $KEY_PATH quizxmentor.tar $EC2_USER@$EC2_HOST:~/
scp -i $KEY_PATH .env $EC2_USER@$EC2_HOST:~/

# Deploy on EC2
echo "Deploying on EC2..."
ssh -i $KEY_PATH $EC2_USER@$EC2_HOST << 'EOF'
    # Load Docker image
    docker load < quizxmentor.tar
    
    # Stop and remove existing container
    docker stop quizapp || true
    docker rm quizapp || true
    
    # Run new container
    docker run -d --name quizapp -p 5000:5000 --env-file .env quizxmentor
    
    # Clean up
    rm quizxmentor.tar
    
    echo "Deployment completed successfully!"
    echo "Application is running at: http://43.204.141.56:5000"
EOF

# Clean up local files
rm quizxmentor.tar

echo "Deployment script completed!"