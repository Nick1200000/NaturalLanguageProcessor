pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        DATABASE_URL = credentials('database-url')
        DOCKER_REGISTRY = credentials('docker-registry-url')
        DOCKER_CREDS = credentials('docker-hub-credentials')
        KUBE_CONFIG = credentials('kube-config')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'apt-get update && apt-get install -y build-essential docker.io kubectl'
                sh 'pip install --upgrade pip'
                sh 'pip install -e .'
                sh 'python -m nltk.downloader punkt stopwords vader_lexicon averaged_perceptron_tagger maxent_ne_chunker words wordnet'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
        
        stage('Build') {
            when {
                branch 'main'
            }
            steps {
                sh 'echo $DOCKER_CREDS_PSW | docker login -u $DOCKER_CREDS_USR --password-stdin $DOCKER_REGISTRY'
                sh 'docker build -t $DOCKER_REGISTRY/nlp-analyzer:$BUILD_NUMBER -t $DOCKER_REGISTRY/nlp-analyzer:latest .'
                sh 'docker push $DOCKER_REGISTRY/nlp-analyzer:$BUILD_NUMBER'
                sh 'docker push $DOCKER_REGISTRY/nlp-analyzer:latest'
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                sh 'mkdir -p ~/.kube'
                sh 'echo "$KUBE_CONFIG" > ~/.kube/config'
                sh 'kubectl config use-context staging'
                sh 'kubectl set image deployment/nlp-analyzer nlp-analyzer=$DOCKER_REGISTRY/nlp-analyzer:$BUILD_NUMBER --record'
                sh 'kubectl rollout status deployment/nlp-analyzer'
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Yes, deploy to production"
            }
            steps {
                sh 'kubectl config use-context production'
                sh 'kubectl set image deployment/nlp-analyzer nlp-analyzer=$DOCKER_REGISTRY/nlp-analyzer:$BUILD_NUMBER --record'
                sh 'kubectl rollout status deployment/nlp-analyzer'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}