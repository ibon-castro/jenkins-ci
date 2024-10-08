pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iboncas/app'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository using the 'github' credentials
                git credentialsId: 'github', branch:'master', url: 'https://github.com/ibon-castro/jenkins-ci.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    }
                    sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                script {
                    // Pull and run the Docker image locally
                    sh """
                    docker run -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                    docker run --rm ghcr.io/zaproxy/zaproxy:weekly /usr/bin/curl http://localhost:5000
                    """
                }
            }
        }
    }
}
