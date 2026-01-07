# cicd-jenkins-ds
Proyecto individual CI/CD con Jenkins (tests + SonarQube + Trivy + DockerHub) aplicado a un mini pipeline de ciencia de datos en Python.

## Setup local
Cómo crear venv
* pip install -r requirements.txt

Hacer test del train
* pytest -q

## Docker
Dockerizar proyecto 
* docker build -t cicd-jenkins-ds:local .
* docker run --rm cicd-jenkins-ds:local

## CI/CD
La integración Jenkins + SonarQube + Trivy + DockerHub se implementa en la US-03 (Jenkinsfile y evidencias en PR).