pipeline {
    agent any
    environment {
        scannerHome = tool 'SonarScanner'
        DOCKERHUB = credentials('dockerhub')
        SSH_KEY = credentials('ssh_key')
    }
    stages {
        stage('Scan') {
            steps {
                withSonarQubeEnv('SonarCloud') {
                    sh "${scannerHome}/bin/sonar-scanner \
                    -Dsonar.projectKey=thuanlee215_schat \
                    -Dsonar.organization=thuanlee215 \
                    -Dsonar.inclusions=*,backend/**"
                }
            }
        }
        stage('Build') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    sh 'docker compose build'
                    sh 'echo $DOCKERHUB_PSW | docker login -u $DOCKERHUB_USR --password-stdin'
                    sh 'docker compose push'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    ssh -i $SSH_KEY -o StrictHostKeyChecking=no ubuntu@16.162.46.190 \
                    "docker compose down --volumes && \
                    docker compose pull && \
                    echo 'Y' | docker image prune && \
                    docker compose up -d && \
                    exit"
                '''
            }
        }
    }
    post {
        success {
            echo 'Check deployment on http://16.162.46.190:8000'
        }
        always {
            sh 'echo "Y" | docker image prune'
            sh 'docker logout'
            echo 'See you again!!'
        }
    }
}
