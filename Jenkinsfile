pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iboncas/app'
        IMAGE_TAG = 'latest'
        REPORT_DIR = '/var/lib/jenkins/workspace/pipeline/zap-reports'
        NETWORK_NAME = 'zap-network'
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository using the 'github' credentials
                git credentialsId: 'github', branch: 'master', url: 'https://github.com/ibon-castro/jenkins-ci.git'
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

        stage('Run ZAP Scan') {
            steps {
                script {
                    // Create the report directory and ensure permissions
                    sh "mkdir -p ${REPORT_DIR}"
                    sh "chmod 777 ${REPORT_DIR}"

                    // Run ZAP with volume and network configurations
                    sh """
                    docker run --rm --network ${NETWORK_NAME} -v ${REPORT_DIR}:/zap/wrk ghcr.io/zaproxy/zaproxy:weekly \
                    zap-baseline.py -t http://my_app:5000 -r zap_report.html
                    """
                }
            }
        }

        stage('Archive ZAP Report') {
            steps {
                archiveArtifacts artifacts: 'zap-reports/zap_report.html'
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
