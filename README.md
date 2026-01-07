# cicd-jenkins-ds
Proyecto individual CI/CD con Jenkins (tests + SonarQube + Trivy + DockerHub) aplicado a un mini pipeline de ciencia de datos en Python.

Cómo crear venv
* pip install -r requirements.txt
* pytest -q
* docker build -t cicd-jenkins-ds:local .
* docker run --rm cicd-jenkins-ds:local