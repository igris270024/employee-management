pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t employee-management .'
            }
        }

        stage('Deploy Container') {
            steps {
                bat '''
                    docker stop employee-app >NUL 2>&1
                    docker rm employee-app >NUL 2>&1
                    docker run -d -p 5000:5000 --name employee-app employee-management
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD PIPELINE SUCCESSFUL!'
            echo 'Application deployed successfully.'
        }
        failure {
            echo 'BUILD FAILED!'
        }
    }
}