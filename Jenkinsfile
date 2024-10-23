pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iboncas/app'
        IMAGE_TAG = 'latest'
        NETWORK_NAME = 'network'
        REPO = 'https://github.com/ibon-castro/jenkins-ci.git'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository using the 'github' credentials
                git credentialsId: 'github', branch: 'master', url: "${REPO}"
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

        stage('Deploy on K8S') {
            steps {
                withCredentials([string(credentialsId: 'my_kubernetes', variable: 'api_token')]) {
                    sh 'kubectl --token $api_token --server https://192.168.49.2:8443 --insecure-skip-tls-verify=true apply -f deployment.yaml'
                }
            }
        }
    }
}
