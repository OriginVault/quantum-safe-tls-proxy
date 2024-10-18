
# Quantum Safe TLS Proxy

## Overview

The Quantum Safe TLS Proxy is a secure reverse proxy designed to future-proof data protection using quantum-safe cryptographic algorithms. The project supports deployment on various cloud platforms and is integrated with monitoring and automated deployment capabilities.

## Features

- **Quantum-Safe Encryption**: Uses post-quantum cryptographic algorithms such as Kyber, Dilithium, and Falcon to secure data.
- **TLS Termination**: Acts as a gateway for incoming requests, handling TLS termination and routing.
- **Monitoring and Metrics**: Integrates with Prometheus for real-time monitoring of metrics such as request count, latency, and active connections.
- **Automatic Certificate Renewal**: Supports automatic renewal of TLS certificates using Certbot or custom scripts.
- **Rate Limiting and Authentication**: Implements middleware for rate limiting and authentication for enhanced security.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.9+
- Prometheus server (for monitoring)

## Quickstart

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/quantum-safe-tls-proxy.git
   cd quantum-safe-tls-proxy
   ```

2. **Copy the `.env` file and update the configuration**
   ```bash
   cp .env.example .env
   ```

3. **Build the Docker image**
   ```bash
   docker build -t quantum-safe-tls-proxy .
   ```

4. **Run the Docker container**
   ```bash
   docker run -d -p 443:443 -p 9090:9090 --env-file .env quantum-safe-tls-proxy
   ```

5. **Access the proxy**
   - The proxy will be available at `https://localhost:443`.

## Configuration

### .env File

The `.env` file contains various environment variables that control the behavior of the application. Here is an example of what it might look like:

```plaintext
APP_ENV=dev
PROXY_HOST=0.0.0.0
PROXY_PORT=443
TLS_CERT_FILE=./config/tls/cert.pem
TLS_KEY_FILE=./config/tls/key.pem
TLS_CA_FILE=./config/tls/ca.pem
METRICS_PORT=9090
ENABLE_AUTO_RENEWAL=true
RENEWAL_CHECK_INTERVAL=7d
LOG_LEVEL=DEBUG
BACKEND_URL=http://localhost:8080
AUTH_SECRET_KEY=my_secret_key
RATE_LIMIT=100
RATE_LIMIT_WINDOW=60
```

### Docker Configuration

A `Dockerfile` is provided for building the project as a Docker container. You can also use the provided `docker-compose.yml` file to run the application.

## Running Tests

To run the tests, use the following command:

```bash
./ci/scripts/run_tests.sh
```

This will execute unit tests and provide coverage reports.

## Monitoring and Metrics

The project integrates with Prometheus for monitoring. A metrics server is exposed on port 9090 by default. You can customize the metrics collection and alerting rules using the Prometheus configuration files located in `monitoring/prometheus/`.

## Deployment

The deployment can be automated using GitHub Actions or GitLab CI. The `ci/` directory contains configuration files for both CI/CD systems:

- GitHub Actions: `ci/github/.github/workflows/ci.yml`
- GitLab CI: `ci/gitlab/.gitlab-ci.yml`

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`feature/your-feature-name`).
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the maintainers at `maintainer@quantumsafetlsproxy.org`.
