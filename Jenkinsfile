pipeline {
  agent any

  options { timestamps() }

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
          set -e
          docker run --rm \
            -v jenkins_home:/var/jenkins_home \
            -w "$WORKSPACE" \
            python:3.11-slim bash -lc "
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
          sh '''
            set -e
            docker run --rm \
              -v jenkins_home:/var/jenkins_home \
              -w "$WORKSPACE" \
              -e SONAR_HOST_URL \
              -e SONAR_AUTH_TOKEN \
              sonarsource/sonar-scanner-cli:latest
          '''
        }
      }
    }

    stage('Build Docker') {
      steps {
        sh '''
          set -e
          docker build -t "$IMAGE" .
          docker tag "$IMAGE" "$DOCKERHUB_REPO:latest"
        '''
      }
    }

    stage('Trivy (security image)') {
      steps {
        sh '''
          set -e
          docker run --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v trivy-cache:/root/.cache/ \
            aquasec/trivy:latest image \
              --exit-code 1 --severity HIGH,CRITICAL \
              "$IMAGE"
        '''
      }
    }

    stage('Login DockerHub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
          sh '''
            set -e
            echo "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin
          '''
        }
      }
    }

    stage('Push DockerHub') {
      steps {
        sh '''
          set -e
          docker push "$IMAGE"
          docker push "$DOCKERHUB_REPO:latest"
        '''
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}


