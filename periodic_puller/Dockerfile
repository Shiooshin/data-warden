FROM python:3.9-slim

ENV PYTHONPATH "${PYTHONPATH}:/app/"

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc g++ libpq-dev python-dev librocksdb-dev libgflags-dev libsnappy-dev zlib1g-dev libbz2-dev libzstd-dev liblz4-dev
RUN pip install -r requirements.txt
COPY . /app

CMD ["python", "/app/puller.py"]