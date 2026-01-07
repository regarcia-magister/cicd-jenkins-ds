FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements.txt

COPY app /app/app
COPY pytest.ini /app/pytest.ini
COPY tests /app/tests

# Comando por defecto: ejecutar el pipeline (train + métricas) y dejarlo como evidencia
CMD ["python", "-m", "app.main", "--out", "artifacts/metrics.json"]
