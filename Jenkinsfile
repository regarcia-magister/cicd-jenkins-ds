pipeline {
  agent any

  options {
    timestamps()
  }

  environment {
    DOCKERHUB_REPO = "regarciaceste/cicd-jenkins-ds"
    SONARQUBE_ENV  = "SonarQube"
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
        script {
          env.SHORT_SHA = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
          env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.SHORT_SHA}"
          env.IMAGE     = "${env.DOCKERHUB_REPO}:${env.IMAGE_TAG}"
        }
      }
    }

    stage('Tests') {
      steps {
        sh '''
          docker run --rm -v "$PWD:/work" -w /work python:3.11-slim bash -lc "
            pip install -U pip &&
            pip install -r requirements.txt &&
            pytest -q
          "
        '''
      }
    }

    stage('SonarQube (quality)') {
      steps {
        withSonarQubeEnv("${SONARQUBE_ENV}") {
          sh 'sonar-scanner'
        }
      }
    }

    stage('Build Docker') {
      steps {
        sh 'docker build -t "$IMAGE" .'
        sh 'docker tag "$IMAGE" "$DOCKERHUB_REPO:latest"'
      }
    }

    stage('Trivy (security image)') {
      steps {
        sh '''
          docker run --rm aquasec/trivy:latest image \
            --exit-code 1 --severity HIGH,CRITICAL \
            "$IMAGE"
        '''
      }
    }

    stage('Login DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
          sh 'echo "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin'
        }
      }
    }

    stage('Push DockerHub') {
      steps {
        sh 'docker push "$IMAGE"'
        sh 'docker push "$DOCKERHUB_REPO:latest"'
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}

