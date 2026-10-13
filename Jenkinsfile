pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t employee-management .'
            }
        }

        stage('Deploy Container') {
            steps {
                sh '''
                    docker stop employee-app >/dev/null 2>&1 || true
                    docker rm employee-app >/dev/null 2>&1 || true
                    docker run -d -p 5000:5000 --name employee-app employee-management
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded; application deployed.'
        }
        failure {
            echo 'Build failed. Check the stage errors in Console Output.'
        }
    }
}