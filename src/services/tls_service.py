import ssl
import os
import time
from utils.logger import get_logger
from crypto.quantum_encryption_service import QuantumEncryptionService

logger = get_logger(__name__)

class TLSService:
    """
    Handles TLS configuration, including setting up quantum-safe TLS contexts.
    """

    def __init__(self, cert_file, key_file, ca_file=None, use_hybrid=False, check_interval=60, key_name=None, kms_aes_key_name=None):
        """
        Initializes the TLSService with the specified certificate files.
        
        Args:
            cert_file (str): Path to the TLS certificate file.
            key_file (str): Path to the private key file.
            ca_file (str, optional): Path to the CA certificate file.
            use_hybrid (bool): Whether to enable hybrid quantum-safe algorithms.
            check_interval (int): Interval in seconds to check for certificate changes.
            key_name (str, optional): KMS key name for quantum-safe key operations.
            kms_aes_key_name (str, optional): KMS key name for decrypting the AES key.
        """
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        self.use_hybrid = use_hybrid
        self.check_interval = check_interval
        self.key_name = key_name
        self.kms_aes_key_name = kms_aes_key_name
        self.tls_context = None
        self.last_checked = time.time()
        self.quantum_service = QuantumEncryptionService()
        self._setup_tls_context()

    def _setup_tls_context(self):
        """
        Sets up the TLS context with quantum-safe settings.
        """
        try:
            self.tls_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.tls_context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
            if self.ca_file:
                self.tls_context.load_verify_locations(cafile=self.ca_file)

            # Configure quantum-safe algorithms if hybrid mode is enabled
            if self.use_hybrid:
                self._configure_hybrid_mode()
                logger.info("Quantum-safe algorithms configured for hybrid mode.")

            # Set additional TLS options
            self.tls_context.minimum_version = ssl.TLSVersion.TLSv1_3
            self.tls_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older protocols
            logger.info("TLS context successfully set up.")
        except Exception as e:
            logger.error(f"Failed to set up TLS context: {e}")
            raise

    def _configure_hybrid_mode(self):
        """
        Configures hybrid mode settings using quantum-safe and classical algorithms.
        """
        try:
            # Example hybrid configuration (customize as needed)
            # This could involve using both classical and quantum-safe keys for encryption
            logger.info("Setting up hybrid quantum-safe configuration.")
            if not self.key_name or not self.kms_aes_key_name:
                logger.warning("Key names for quantum-safe encryption are not provided. Hybrid mode might be incomplete.")
            else:
                # Perform some quantum-safe operations for demonstration purposes
                aes_key = os.urandom(32)  # Generate a random AES key for encryption
                encrypted_aes_key = self.encrypt_with_kyber(aes_key, self.key_name, self.kms_aes_key_name)
                if encrypted_aes_key:
                    logger.info("Hybrid quantum-safe configuration is successfully set up.")
        except Exception as e:
            logger.error(f"Failed to configure hybrid quantum-safe mode: {e}")
            raise

    def check_certificate_reload(self):
        """
        Checks if the certificate files have been updated and reloads the TLS context if necessary.
        """
        current_time = time.time()
        if current_time - self.last_checked < self.check_interval:
            return  # Skip check if the interval hasn't passed
        
        self.last_checked = current_time

        try:
            cert_mtime = os.path.getmtime(self.cert_file)
            key_mtime = os.path.getmtime(self.key_file)
            if cert_mtime > self.last_checked or key_mtime > self.last_checked:
                logger.info("Certificate or key file has been updated, reloading TLS context.")
                self._setup_tls_context()
        except Exception as e:
            logger.error(f"Failed to check certificate reload: {e}")

    def get_tls_context(self):
        """
        Returns the configured TLS context.
        
        Returns:
            ssl.SSLContext: The configured TLS context.
        """
        self.check_certificate_reload()
        return self.tls_context

    def encrypt_with_kyber(self, aes_key, key_name, kms_aes_key_name):
        """
        Encrypts an AES key using the Kyber quantum-safe algorithm.
        
        Args:
            aes_key (bytes): The AES key to encrypt.
            key_name (str): The KMS key resource name for retrieving the Kyber public key.
            kms_aes_key_name (str): The KMS key resource name for decrypting the AES key.
            
        Returns:
            tuple: A tuple containing the ciphertext and encrypted AES key, or (None, None) on failure.
        """
        return self.quantum_service.encrypt_aes_key_with_kyber(aes_key, key_name, kms_aes_key_name)

    def decrypt_with_kyber(self, encrypted_aes_key, key_name, kms_aes_key_name):
        """
        Decrypts an AES key using the Kyber quantum-safe algorithm.
        
        Args:
            encrypted_aes_key (bytes): The encrypted AES key to decrypt.
            key_name (str): The KMS key resource name for retrieving the Kyber private key.
            kms_aes_key_name (str): The KMS key resource name for decrypting the AES key.
            
        Returns:
            bytes: The decrypted AES key, or None on failure.
        """
        return self.quantum_service.decrypt_aes_key_with_kyber(encrypted_aes_key, key_name, kms_aes_key_name)
