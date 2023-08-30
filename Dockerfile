# Set base image (host OS)
FROM python:3.8-slim

# Update CA certificates (optional)
RUN update-ca-certificates

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    curl

# Copy the content of the local src directory to the working directory
COPY / .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV development
ENV ROOMS_FILES_PATH rooms/

# Define a health check for the container
HEALTHCHECK --interval=10s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

# Specify the command to run on container start
CMD [ "python", "./chatApp.py" ]
