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

Este proyecto incluye un pipeline CI/CD definido en `Jenkinsfile` con las etapas:
1. Checkout
2. Tests (pytest)
3. SonarQube (calidad)
4. Build Docker
5. Trivy (seguridad de imagen)
6. Login DockerHub
7. Push DockerHub

### Disparo del pipeline
El job en Jenkins está configurado con **Poll SCM**:
- `H/5 * * * *` (cada 5 minutos)

### Requisitos en Jenkins (configuración)
- **SonarQube server** configurado en Jenkins (Manage Jenkins → System).
- **Credenciales** requeridas:
  - `sonar-token` (Secret text)
  - `dockerhub-creds` (Username + token)

### Publicación
La imagen se publica en DockerHub y queda disponible con:
- un tag versionado por build (ej. `BUILD_NUMBER-SHORT_SHA`)
- y el tag `latest`.
