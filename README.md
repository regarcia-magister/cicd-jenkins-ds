# cicd-jenkins-ds
Proyecto individual CI/CD con Jenkins (tests + SonarQube + Trivy + DockerHub) aplicado a un mini pipeline de ciencia de datos en Python.

Cómo crear venv
* pip install -r requirements.txt

Hacer test del train
* pytest -q

Dockerizar proyecto 
* docker build -t cicd-jenkins-ds:local .
* docker run --rm cicd-jenkins-ds:local