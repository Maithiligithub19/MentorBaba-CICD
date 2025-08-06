pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'quizxmentor'
        CONTAINER_NAME = 'quizapp'
        PORT = "5000"
        EMAIL = "maithilisude19@gmail.com"
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/Maithiligithub19/MentorBaba-CICD.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }
        
        stage('Stop & Remove Previous Container') {
            steps {
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                '''
            }
        }
        
        stage('Run Container') {
            steps {
                sh 'docker run -d --name $CONTAINER_NAME -p $PORT:5000 --env-file /home/ubuntu/.env $IMAGE_NAME'
            }
        }
        
        stage('Send Email Notification') {
            steps {
                emailext (
                    subject: "QuizXMentor App Deployed Successfully!",
                    body: "Your Flask Quiz App is deployed! http://ec2-43-204-141-56:${PORT}/",
                    to: "${EMAIL}"
                )
            }
        }
    }
}