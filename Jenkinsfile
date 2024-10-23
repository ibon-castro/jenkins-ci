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

        stage('Deploy Locally') {
            steps {
                script {
                    // Create a Docker network and deploy the app on that network
                    sh """
                    docker network create ${NETWORK_NAME}
                    docker run -d --name my_app --network ${NETWORK_NAME} -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Stop App') {
            steps {
                script {
                    // Stop and clean up the app container and network
                    sh """
                    docker stop my_app
                    docker rm my_app
                    docker network rm ${NETWORK_NAME}
                    """
                }
            }
        }
    }
}
