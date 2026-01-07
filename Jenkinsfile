pipeline {
  agent any

  environment {
    SONARQUBE_SERVER = 'sonarqube-local'
    DOCKERHUB_REPO   = 'regarciaceste/cicd-jenkins-ds'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install deps') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Tests') {
      steps {
        sh 'pytest -q'
      }
    }

    stage('SonarQube') {
      steps {
        withSonarQubeEnv("${SONARQUBE_SERVER}") {
          sh 'sonar-scanner'
        }
      }
    }

    stage('Trivy (fs)') {
      steps {
        sh 'docker run --rm -v "$PWD:/work" aquasec/trivy:latest fs --exit-code 0 --severity HIGH,CRITICAL /work'
      }
    }

    stage('Docker build') {
      steps {
        sh 'docker build -t cicd-jenkins-ds:ci .'
      }
    }

    // Push lo activamos cuando confirmemos credenciales en Jenkins
  }
}
