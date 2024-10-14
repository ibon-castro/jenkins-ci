pipeline {
    agent any

    environment {
        IMAGE_NAME = 'iboncas/app'
        IMAGE_TAG = 'latest'
        NETWORK_NAME = 'network'
        DEFECTDOJO_URL = 'https://defectdojo.example.com'
        DEFECTDOJO_PRODUCT_ID = 'jenkins'
        DEFECTDOJO_ENGAGEMENT_ID = 'sonarqube'
        SCAN_TYPE = 'SonarQube Scan'
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

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv() {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
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

        stage('DefectDojo Integration') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'defectdojo_api', variable: 'DEFECTDOJO_API_KEY')]) {
                        sh """
                        defectdojo-api --url ${DEFECTDOJO_URL} --api-key ${DEFECTDOJO_API_KEY} --scan-type ${SCAN_TYPE} --product-id ${DEFECTDOJO_PRODUCT_ID} --engagement-id ${DEFECTDOJO_ENGAGEMENT_ID} --file-path sonarqube-results.xml
                        """
                    }
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
