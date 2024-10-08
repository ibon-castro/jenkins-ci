pipeline {
    agent any

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
                    // Log in to Docker Hub using the 'dockerhub' credentials
                    sh "echo ${DOCKER_CREDENTIALS_PSW} | docker login -u ${DOCKER_CREDENTIALS_USR} --password-stdin"
                    // Build the Docker image
                    docker.build('registration-app')
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                script {
                    // Tag and push the image to Docker Hub
                    sh "docker tag registration-app ${DOCKER_CREDENTIALS_USR}/registration-app:latest"
                    sh "docker push ${DOCKER_CREDENTIALS_USR}/registration-app:latest"
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    // Stop and remove any existing container
                    sh 'docker stop registration-app || true && docker rm registration-app || true'
                    // Run the new container
                    sh 'docker run -d -p 5000:5000 --name registration-app ${DOCKER_CREDENTIALS_USR}/registration-app:latest'
                }
            }
        }
    }
}
