pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iboncas/app'
        IMAGE_TAG = 'latest'
        REPORT_DIR = './zap-reports'
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
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy Locally') {
            steps {
                script {
                    // Run the app in detached mode
                    sh "docker run -d --name my_app -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}"

                    // Wait for the app to be ready
                    sh "sleep 5"
                }
            }
        }

        stage('Run ZAP Scan') {
            steps {
                script {
                    // Create a directory for ZAP reports and set permissions
                    sh "mkdir -p ${REPORT_DIR}"
                    sh "chmod 777 ${REPORT_DIR}"

                    // Run ZAP and mount the report directory with full permissions
                    sh """
                    docker run --rm -v \$(pwd)/${REPORT_DIR}:/zap/wrk ghcr.io/zaproxy/zaproxy:weekly \
                    zap-baseline.py -t http://localhost:5000 -r /zap/wrk/zap_report.html
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

    post {
        always {
            // Archive the ZAP report as an artifact in Jenkins
            archiveArtifacts artifacts: "${REPORT_DIR}/zap_report.html", allowEmptyArchive: true
