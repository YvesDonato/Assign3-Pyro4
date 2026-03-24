# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY mysocketserver.py .

# Install Pyro4
RUN pip install Pyro4

# Run the Python script when the container starts
CMD ["python", "mysocketserver.py"]