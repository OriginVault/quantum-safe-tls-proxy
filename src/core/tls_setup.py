import os
from services.tls_service import TLSService
from config.config_loader import load_config
from utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_CONFIG = {
    'tls': {
        'cert_file': 'config/tls/cert.pem',
        'key_file': 'config/tls/key.pem',
        'ca_file': None,
        'use_hybrid': False,
        'check_interval': 60
    },
    'quantum': {
        'key_name': None,
        'kms_aes_key_name': None
    }
}

def setup_tls_service():
    """
    Sets up the TLS service with the appropriate configuration.

    Returns:
        TLSService: An instance of the TLSService configured with the specified parameters.
    """
    try:
        # Load configuration with fallback to default values
        config = load_config() or {}
        tls_config = config.get('tls', DEFAULT_CONFIG['tls'])
        quantum_config = config.get('quantum', DEFAULT_CONFIG['quantum'])

        # Validate required TLS parameters
        cert_file = tls_config.get('cert_file')
        key_file = tls_config.get('key_file')
        if not os.path.isfile(cert_file) or not os.path.isfile(key_file):
            logger.error(f"Missing or invalid TLS certificate/key file: cert_file={cert_file}, key_file={key_file}")
            raise FileNotFoundError("TLS certificate or key file is not found or accessible.")

        # Extract parameters with fallbacks
        ca_file = tls_config.get('ca_file', DEFAULT_CONFIG['tls']['ca_file'])
        use_hybrid = tls_config.get('use_hybrid', DEFAULT_CONFIG['tls']['use_hybrid'])
        check_interval = tls_config.get('check_interval', DEFAULT_CONFIG['tls']['check_interval'])
        key_name = quantum_config.get('key_name', DEFAULT_CONFIG['quantum']['key_name'])
        kms_aes_key_name = quantum_config.get('kms_aes_key_name', DEFAULT_CONFIG['quantum']['kms_aes_key_name'])

        # Log the configuration being used (do not log sensitive data)
        logger.info(f"Setting up TLS service with cert_file: {cert_file}, key_file: {key_file}, "
                    f"ca_file: {ca_file}, use_hybrid: {use_hybrid}, check_interval: {check_interval}")

        # Initialize the TLS service
        tls_service = TLSService(
            cert_file=cert_file,
            key_file=key_file,
            ca_file=ca_file,
            use_hybrid=use_hybrid,
            check_interval=check_interval,
            key_name=key_name,
            kms_aes_key_name=kms_aes_key_name
        )

        logger.info("TLS service setup completed successfully.")
        return tls_service

    except FileNotFoundError as fnf_error:
        logger.critical(f"TLS setup failed due to missing file: {fnf_error}")
        raise
    except Exception as e:
        logger.error(f"Failed to set up TLS service: {e}", exc_info=True)
        raise

def get_tls_context():
    """
    Gets the TLS context from the configured TLS service.

    Returns:
        ssl.SSLContext: The configured TLS context.
    """
    try:
        # Set up the TLS service
        tls_service = setup_tls_service()

        # Retrieve the TLS context
        tls_context = tls_service.get_tls_context()
        logger.info("TLS context retrieved successfully.")
        return tls_context

    except Exception as e:
        logger.error(f"Error getting TLS context: {e}", exc_info=True)
        raise

def dynamic_reload_config():
    """
    Dynamically reloads the TLS configuration.
    Useful for situations where configuration changes need to be applied without restarting the service.
    """
    try:
        logger.info("Attempting to dynamically reload TLS configuration.")
        tls_service = setup_tls_service()
        logger.info("TLS configuration dynamically reloaded successfully.")
        return tls_service
    except Exception as e:
        logger.error(f"Failed to dynamically reload TLS configuration: {e}", exc_info=True)
        return None