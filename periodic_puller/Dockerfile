FROM python:3.8.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ../. /app

CMD ["python", "/app/periodic_puller/puller.py"]