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
    build-essential \
    cmake \
    git \
    python3-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Prometheus client library
RUN pip install prometheus_client

# Build and install OpenSSL from source
RUN git clone https://github.com/openssl/openssl.git && \
    cd openssl && \
    git checkout openssl-3.0.0 && \
    ./config && \
    make -j$(nproc) && \
    make install

# Clone and build oqs-openssl
RUN git clone --branch openssl-3.0.0 https://github.com/open-quantum-safe/oqs-openssl.git && \
    cd oqs-openssl && \
    ./config && \
    make -j$(nproc) && \
    make install

# Update the library path to include oqs-openssl and liboqs
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Clone and build the LibOQS Python bindings
RUN git clone --recursive https://github.com/open-quantum-safe/liboqs-python.git /liboqs-python && \
    cd /liboqs-python && \
    python3 setup.py build && \
    python3 setup.py install

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
