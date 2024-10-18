from oqs import Signature, KeyEncapsulation
from utils.logger import get_logger
from crypto.key_management import load_private_key

logger = get_logger(__name__)

class QuantumSafeCrypto:
    """
    Handles post-quantum cryptographic operations using OQS.
    """
    
    def __init__(self, algorithm="Dilithium3", kem_algorithm="Kyber512"):
        """
        Initializes the QuantumSafeCrypto class with the specified algorithms.
        
        Args:
            algorithm (str): The post-quantum signature algorithm (e.g., "Dilithium3").
            kem_algorithm (str): The key encapsulation mechanism (KEM) algorithm (e.g., "Kyber512").
        """
        self.algorithm = algorithm
        self.kem_algorithm = kem_algorithm
        self.signature_scheme = None
        self.kem_scheme = None
        self._initialize_algorithms()

    def _initialize_algorithms(self):
        """
        Initializes the signature and KEM algorithms.
        """
        try:
            self.signature_scheme = Signature(self.algorithm)
            self.kem_scheme = KeyEncapsulation(self.kem_algorithm)
            logger.info(f"Initialized post-quantum algorithms: {self.algorithm}, {self.kem_algorithm}")
        except Exception as e:
            logger.error(f"Failed to initialize algorithms: {self.algorithm}, {self.kem_algorithm} | {e}")
            raise

    def generate_keypair(self):
        """
        Generates a key pair for the chosen signature scheme.
        
        Returns:
            tuple: A tuple containing (public_key, private_key).
        """
        try:
            public_key, private_key = self.signature_scheme.generate_keypair()
            logger.info(f"Generated key pair for algorithm {self.algorithm}")
            return public_key, private_key
        except Exception as e:
            logger.error(f"Error generating key pair: {e}")
            raise

    def sign_message(self, message, private_key_source, password=None):
        """
        Signs a message using the private key loaded from the specified source.
        
        Args:
            message (bytes): The message to sign.
            private_key_source (str): The source from which to load the private key (e.g., file path).
            password (str, optional): Password for decrypting the private key if needed.
        
        Returns:
            bytes: The signature.
        """
        try:
            private_key = load_private_key(private_key_source, password)
            signature = self.signature_scheme.sign(message, private_key)
            logger.info("Message successfully signed.")
            return signature
        except Exception as e:
            logger.error(f"Error signing message: {e}")
            raise

    def verify_signature(self, message, signature, public_key):
        """
        Verifies a signature for a given message and public key.
        
        Args:
            message (bytes): The original message.
            signature (bytes): The signature to verify.
            public_key (bytes): The public key used for verification.
        
        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        try:
            is_valid = self.signature_scheme.verify(message, signature, public_key)
            logger.info("Signature verification result: " + ("valid" if is_valid else "invalid"))
            return is_valid
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            raise

    def generate_kem_keypair(self):
        """
        Generates a key pair for the chosen KEM algorithm.
        
        Returns:
            tuple: A tuple containing (public_key, private_key).
        """
        try:
            public_key, private_key = self.kem_scheme.generate_keypair()
            logger.info(f"Generated KEM key pair for algorithm {self.kem_algorithm}")
            return public_key, private_key
        except Exception as e:
            logger.error(f"Error generating KEM key pair: {e}")
            raise

    def encapsulate(self, public_key):
        """
        Encapsulates a shared secret using the public key.
        
        Args:
            public_key (bytes): The public key for encapsulation.
        
        Returns:
            tuple: A tuple containing (ciphertext, shared_secret).
        """
        try:
            ciphertext, shared_secret = self.kem_scheme.encapsulate(public_key)
            logger.info("Encapsulation successful.")
            return ciphertext, shared_secret
        except Exception as e:
            logger.error(f"Error during encapsulation: {e}")
            raise

    def decapsulate(self, ciphertext, private_key_source, password=None):
        """
        Decapsulates the shared secret using the private key loaded from the specified source.
        
        Args:
            ciphertext (bytes): The ciphertext containing the encapsulated secret.
            private_key_source (str): The source from which to load the private key (e.g., file path).
            password (str, optional): Password for decrypting the private key if needed.
        
        Returns:
            bytes: The shared secret.
        """
        try:
            private_key = load_private_key(private_key_source, password)
            shared_secret = self.kem_scheme.decapsulate(ciphertext, private_key)
            logger.info("Decapsulation successful.")
            return shared_secret
        except Exception as e:
            logger.error(f"Error during decapsulation: {e}")
            raise
