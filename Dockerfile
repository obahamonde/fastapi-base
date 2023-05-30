FROM python:3.9.7-slim-buster

ARG LOCAL_PATH

WORKDIR /app

COPY ${LOCAL_PATH} /app

RUN pip install -r requirements.txt
EXPOSE 8080

# Run uvicorn when the container launches

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
