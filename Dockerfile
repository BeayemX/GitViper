FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN cd /app && pip install --no-cache-dir -r requirements.txt

COPY ./src/ /app/

WORKDIR /repo
ENTRYPOINT ["python", "/app/main.py"]
