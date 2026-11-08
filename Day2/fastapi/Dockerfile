
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Commands to build and run the Docker container:
# 1. Build the Docker image:
#    docker build -t fastapi .
# 2. Run the Docker container:
#    docker run -d -p 8000:8000 --name day2-api fastapi