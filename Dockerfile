FROM python:3.7.4-slim-buster

# Set the working directory to /app

WORKDIR /app

# Copy the current directory contents into the container at /app

COPY . /app

# Install any needed packages specified in requirements.txt

RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8080 available to the world outside this container

EXPOSE 8080

# Run uvicorn when the container launches

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
