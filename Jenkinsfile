pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iboncas/app'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'github', branch: 'master', url: 'https://github.com/ibon-castro/jenkins-ci.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
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
                    // Run the app in detached mode
                    sh "docker run -d --name my_app -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}"

                    // Wait for the app to be ready
                    sh "sleep 10"
                }
            }
        }

        stage('Run ZAP Scan') {
            steps {
                script {
                    // Run ZAP to scan the locally deployed Flask app
                    sh """
                    docker run --rm ghcr.io/zaproxy/zaproxy:weekly zap-baseline.py -t http://localhost:5000 -r zap_report.html
                    """
                }
            }
        }

        stage('Stop App') {
            steps {
                script {
                    // Stop the running app container
                    sh "docker stop my_app"
                }
            }
        }
    }
}
