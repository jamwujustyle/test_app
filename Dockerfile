FROM python:3.11-slim

WORKDIR /test-task

RUN apt-get update && apt-get install -y \
    libpq-dev gcc ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "80002", "--reload"]
