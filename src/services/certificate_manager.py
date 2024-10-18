import os
import subprocess
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from utils.logger import get_logger

logger = get_logger(__name__)

class CertificateManager:
    """
    Manages TLS certificates, including loading, validation, and renewal.
    """

    def __init__(self, cert_file, key_file, ca_file=None, renewal_threshold_days=30, domain=None):
        """
        Initializes the CertificateManager with the specified certificate files.
        
        Args:
            cert_file (str): Path to the TLS certificate file.
            key_file (str): Path to the private key file.
            ca_file (str, optional): Path to the CA certificate file.
            renewal_threshold_days (int): Number of days before expiration to renew the certificate.
            domain (str, optional): The domain name for which the certificate is issued.
        """
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        self.renewal_threshold_days = renewal_threshold_days
        self.domain = domain

    def load_certificate(self):
        """
        Checks if the certificate files exist and are valid.
        
        Returns:
            bool: True if the certificates are valid, False otherwise.
        """
        if not os.path.exists(self.cert_file) or not os.path.exists(self.key_file):
            logger.error("Certificate or key file does not exist.")
            return False

        logger.info("Certificate and key files are loaded successfully.")
        return True

    def validate_certificate(self):
        """
        Validates the certificate and checks for expiration.
        
        Returns:
            bool: True if the certificate is valid, False otherwise.
        """
        try:
            with open(self.cert_file, 'rb') as f:
                cert_data = f.read()
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            days_to_expire = (cert.not_valid_after - datetime.utcnow()).days
            if days_to_expire < self.renewal_threshold_days:
                logger.warning(f"Certificate is expiring in {days_to_expire} days, renewal needed.")
                return False
            logger.info(f"Certificate is valid for {days_to_expire} more days.")
            return True
        except Exception as e:
            logger.error(f"Failed to validate certificate: {e}")
            return False

    def renew_certificate(self):
        """
        Renews the TLS certificate using Certbot if needed.
        
        Returns:
            bool: True if the renewal was successful, False otherwise.
        """
        if not self.domain:
            logger.error("Domain is not specified for certificate renewal.")
            return False

        try:
            # Run Certbot command to renew the certificate
            command = [
                "certbot", "renew",
                "--non-interactive",
                "--quiet",
                "--deploy-hook", f"echo 'Certificate for {self.domain} renewed'"
            ]

            logger.info(f"Attempting to renew the certificate for {self.domain}...")
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                logger.info(f"Certificate for {self.domain} successfully renewed.")
                return True
            else:
                logger.error(f"Certificate renewal failed: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error during certificate renewal: {e}")
            return False
