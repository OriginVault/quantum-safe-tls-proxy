# Use a base image with Python installed
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    libssl-dev \
    curl \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Prometheus client library
RUN pip install prometheus_client

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Make the necessary scripts executable
RUN chmod +x ci/scripts/*.sh

# Expose ports
EXPOSE 443
EXPOSE 9090

# Set environment variables for the container
ENV APP_ENV=production
ENV METRICS_PORT=9090

# Configure the entrypoint
ENTRYPOINT ["./ci/scripts/build_and_deploy.sh"]
