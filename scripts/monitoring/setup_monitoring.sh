#!/bin/bash

# Script to set up monitoring tools
set -euo pipefail

function check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker is not installed. Please install Docker."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        echo "Docker is not running. Please start Docker."
        exit 1
    fi
}

check_docker

echo "Setting up monitoring tools..."

# Start monitoring tools using docker-compose
docker-compose up -d prometheus grafana

echo "Monitoring tools are set up and running."
