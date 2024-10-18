# Quickstart Guide for Quantum Safe TLS Proxy

## Prerequisites
- Docker and Docker Compose installed
- Terraform installed (if using Terraform for deployment)
- Cloud provider account (AWS, Azure, GCP)

## Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/quantum-safe-tls-proxy.git
cd quantum-safe-tls-proxy
```

## Step 2: Generate TLS Certificates
Use the provided script to generate a self-signed certificate:
```bash
./scripts/certs/generate_certs.sh
```
For production, obtain certificates from a trusted CA.

## Step 3: Run Locally (Using Docker Compose)
```bash
docker-compose up -d
```
Access the proxy at `https://localhost`.

## Step 4: Deploy to a Cloud Platform
### AWS
1. Configure AWS credentials:
   ```bash
   aws configure
   ```
2. Deploy using Terraform:
   ```bash
   cd infra/terraform
   terraform init
   terraform apply
   ```
3. Access the service at the provided ALB DNS name.

## Troubleshooting
- **Docker Fails to Start**: Ensure Docker Desktop is running.
- **Certificate Errors**: Make sure the certificate is correctly placed in the `/tls` folder.
