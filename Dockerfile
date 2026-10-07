FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends git gcc libffi-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
