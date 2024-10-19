# Use a base image with Python installed
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies including Nginx
RUN apt-get update && \
    apt-get install -y \
    libssl-dev \
    curl \
    build-essential \
    cmake \
    git \
    nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Build and install liboqs
RUN git clone --recursive https://github.com/open-quantum-safe/liboqs.git && \
    cd liboqs && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_INSTALL_PREFIX=/usr/local .. && \
    make -j$(nproc) && \
    make install

# Clone and build oqs-provider
RUN git clone https://github.com/open-quantum-safe/oqs-provider.git && \
    cd oqs-provider && \
    cmake -B _build -S . && \
    cmake --build _build && \
    cmake --install _build

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Nginx configuration file to the container
COPY config/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy the application code
COPY . /app

# Make sure the Nginx logs directory is writable
RUN mkdir -p /var/log/nginx && \
    chmod -R 755 /var/log/nginx

# Expose the required ports
EXPOSE 443
EXPOSE 9090


# Run Nginx and the Python application together
CMD ["sh", "-c", "echo 'Starting Nginx...' && nginx -g 'daemon off;' & echo 'Starting Python app...' && python ./src/main.py"]
