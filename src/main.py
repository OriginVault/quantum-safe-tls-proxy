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

# Load configuration
def load_config():
    env = os.getenv("APP_ENV", "dev")
    config_file = f"config/env/{env}/config.yaml"
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config

def initialize_services(config):
    # Initialize TLS setup
    tls_setup = TLSSetup(
        cert_file=config["tls"]["cert_file"],
        key_file=config["tls"]["key_file"],
        ca_file=config["tls"]["ca_file"]
    )
    tls_setup.configure_tls()

    # Initialize key management
    key_manager = KeyManager()
    key_manager.load_keys()

    # Initialize backend service communication
    backend_service = BackendService(config["backend"]["url"])

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

    return (tls_setup, key_manager, backend_service, tls_service,
            cert_manager, quantum_handler, auth_handler,
            rate_limiter, health_check)

async def start_proxy(config, tls_setup, backend_service, quantum_handler,
                      auth_handler, rate_limiter, health_check):
    """
    Starts the QuantumSafeProxy.
    """
    proxy = QuantumSafeProxy(
        host=config["proxy"]["host"],
        port=config["proxy"]["port"],
        backend_host=config["backend"]["host"],
        backend_port=config["backend"]["port"],
        cert_file=config["tls"]["cert_file"],
        key_file=config["tls"]["key_file"],
        ca_file=config["tls"].get("ca_file", None)
    )

    # Start the proxy server
    await proxy.start()

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
        (tls_setup, key_manager, backend_service, tls_service,
         cert_manager, quantum_handler, auth_handler, rate_limiter,
         health_check) = initialize_services(config)

        # Optionally enable automatic certificate renewal
        if config["renewal"]["enable_auto_renewal"]:
            renewer = AsyncWorker(cert_manager, tls_service, config["renewal"]["renewal_check_interval"])
            renewer.start()

        # Start the proxy
        asyncio.run(start_proxy(config, tls_setup, backend_service, quantum_handler,
                                auth_handler, rate_limiter, health_check))

    except Exception as e:
        handle_exception(e)

if __name__ == "__main__":
    main()
