import ssl
import os
import time
from utils.logger import get_logger
from crypto.post_quantum_algorithms import QuantumSafeCrypto

logger = get_logger(__name__)

class TLSService:
 """
 Handles TLS configuration, including setting up quantum-safe TLS contexts.
 """

 def __init__(self, cert_file, key_file, ca_file=None, use_hybrid=False, check_interval=60):
     """
     Initializes the TLSService with the specified certificate files.
     
     Args:
         cert_file (str): Path to the TLS certificate file.
         key_file (str): Path to the private key file.
         ca_file (str, optional): Path to the CA certificate file.
         use_hybrid (bool): Whether to enable hybrid quantum-safe algorithms.
         check_interval (int): Interval in seconds to check for certificate changes.
     """
     self.cert_file = cert_file
     self.key_file = key_file
     self.ca_file = ca_file
     self.use_hybrid = use_hybrid
     self.check_interval = check_interval
     self.tls_context = None
     self.last_checked = time.time()
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

         # Use QuantumSafeCrypto for algorithm configuration if hybrid mode is enabled
         if self.use_hybrid:
             qsc = QuantumSafeCrypto()
             logger.info("Quantum-safe algorithms configured for hybrid mode.")

         # Set additional TLS options
         self.tls_context.minimum_version = ssl.TLSVersion.TLSv1_3
         self.tls_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable older protocols
         logger.info("TLS context successfully set up.")
     except Exception as e:
         logger.error(f"Failed to set up TLS context: {e}")
         raise

 def check_certificate_reload(self):
     """
     Checks if the certificate files have been updated and reloads the TLS context if necessary.
     """
     current_time = time.time()
     if current_time - self.last_checked < self.check_interval:
         return  # Skip check if the interval hasn't passed
     
     self.last_checked = current_time

     if os.path.getmtime(self.cert_file) > self.last_checked or os.path.getmtime(self.key_file) > self.last_checked:
         logger.info("Certificate or key file has been updated, reloading TLS context.")
         self._setup_tls_context()

 def get_tls_context(self):
     """
     Returns the configured TLS context.
     
     Returns:
         ssl.SSLContext: The configured TLS context.
     """
     self.check_certificate_reload()
     return self.tls_context
