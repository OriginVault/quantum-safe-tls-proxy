import os
import logging
import yaml
import asyncio
from utils.logger import setup_logging
from core.proxy_handler import QuantumSafeProxy
from core.tls_setup import TLSSetup
from crypto.key_management import KeyManager
from crypto.post_quantum_algorithms import QuantumAlgorithmHandler
from middleware.auth_handler import AuthHandler
from middleware.rate_limiter import RateLimiter
from monitoring.metrics import start_metrics_server, increment_request_counter, \
                               increment_rate_limited_counter, increment_error_counter, \
                               observe_request_latency, set_active_connections
from monitoring.health_check import HealthCheck
from services.backend_service import BackendService
from services.certificate_manager import CertificateManager
from services.tls_service import TLSService
from workers.async_worker import AsyncWorker
from utils.error_handler import handle_exception
from tls_communication import get_tls_certificates_from_service

# Load configuration
def load_config():
    env = os.getenv("APP_ENV", "dev")
    config_file = f"config/env/{env}/config.yaml"
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config

def initialize_services(config):
    # Retrieve public and internal service URLs from the environment variables
    public_service_url = os.getenv("PUBLIC_API_URL")
    internal_service_url = os.getenv("INTERNAL_API_URL")

    if not public_service_url or not internal_service_url:
        raise ValueError("Both PUBLIC_API_URL and INTERNAL_API_URL must be set in environment variables")

    # Initialize backend service communication for public and internal services
    public_backend_service = BackendService(public_service_url)
    internal_backend_service = BackendService(internal_service_url)

    # Retrieve TLS certificates from the TLS Communication Service
    try:
        tls_cert_response = get_tls_certificates_from_service(os.getenv("TLS_COMMUNICATION_SERVICE_URL"))
        cert_file_content = tls_cert_response["cert_file"]
        key_file_content = tls_cert_response["key_file"]
        ca_file_content = tls_cert_response.get("ca_file")

        # Initialize TLS setup with retrieved certificates
        tls_setup = TLSSetup(
            cert_file=cert_file_content,
            key_file=key_file_content,
            ca_file=ca_file_content
        )
        tls_setup.configure_tls()

    except Exception as e:
        logging.error(f"Failed to initialize TLS setup: {e}")
        raise

    # Initialize TLS service for managing certificate lifecycle
    tls_service = TLSService(tls_setup)

    # Initialize certificate manager
    cert_manager = CertificateManager(config)

    # Initialize post-quantum algorithms
    quantum_handler = QuantumAlgorithmHandler()

    # Initialize middleware
    auth_handler = AuthHandler(config["auth"])
    rate_limiter = RateLimiter(config["rate_limiter"])

    # Initialize health checks
    health_check = HealthCheck()

    return (tls_setup, public_backend_service, internal_backend_service, tls_service,
            cert_manager, quantum_handler, auth_handler,
            rate_limiter, health_check)

async def wait_for_tls_updates(tls_setup):
    """
    Listens for incoming connections from the TLS Communication Service
    and dynamically updates the TLS configuration.
    """
    try:
        # This is where the server listens for incoming connections
        # You could use any preferred method to establish this connection
        # For now, this is a placeholder for listening and processing the incoming updates
        logging.info("Waiting for incoming TLS certificate updates...")
        while True:
            # Simulate waiting for an update; replace with actual listening logic
            await asyncio.sleep(60)  # Periodically check for updates
            # If an update is received, you could update the TLS configuration like this:
            tls_setup.configure_tls()
            logging.info("TLS configuration updated successfully.")
    except Exception as e:
        logging.error(f"Error while waiting for TLS updates: {e}")

async def start_proxy(config, tls_setup, public_backend_service, internal_backend_service):
    """
    Starts the QuantumSafeProxy and listens for incoming TLS updates.
    """
    proxy = QuantumSafeProxy(
        host=config["proxy"]["host"],
        port=config["proxy"]["port"]
    )

    # Start the proxy server and TLS update listener concurrently
    await asyncio.gather(
        proxy.start(),
        wait_for_tls_updates(tls_setup)
    )

def main():
    try:
        # Set up logging
        setup_logging("config/logging/log_config.json")

        # Load configuration
        config = load_config()
        logging.info(f"Starting Quantum Safe TLS Proxy in {config['app']['environment']} mode")

        # Start Prometheus metrics server
        start_metrics_server(config["monitoring"]["metrics_port"])

        # Initialize services
        (tls_setup, public_backend_service, internal_backend_service, tls_service,
         cert_manager, quantum_handler, auth_handler, rate_limiter,
         health_check) = initialize_services(config)

        # Optionally enable automatic certificate renewal
        if config["renewal"]["enable_auto_renewal"]:
            renewer = AsyncWorker(cert_manager, tls_service, config["renewal"]["renewal_check_interval"])
            renewer.start()

        # Start the proxy and wait for TLS updates
        asyncio.run(start_proxy(config, tls_setup, public_backend_service, internal_backend_service))

    except Exception as e:
        handle_exception(e)

if __name__ == "__main__":
    main()
