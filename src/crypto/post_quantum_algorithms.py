import oqs
from key_management import load_key_pair_from_kms
from utils.logger import get_logger

# Initialize custom logger
logger = get_logger(__name__)

class QuantumEncryptionService:
    def encrypt_aes_key_with_kyber(self, aes_key, key_name, kms_aes_key_name):
        """
        Encrypt the AES key using a quantum-safe Kyber public key.
        :param aes_key: The AES key to encrypt (in bytes).
        :param key_name: The KMS key resource name for retrieving the Kyber public key.
        :param kms_aes_key_name: The KMS key resource name used to decrypt the AES key.
        :return: A tuple containing the encrypted AES key (ciphertext) and encapsulated shared secret (both in bytes), or None on failure.
        """
        try:
            # Load the Kyber public key from key management
            public_key, _ = load_key_pair_from_kms(key_name, kms_aes_key_name)

            if not public_key:
                raise ValueError("Failed to retrieve Kyber public key.")

            # Use Kyber to encapsulate the secret (AES key)
            with oqs.KeyEncapsulation('Kyber768') as kem:
                # Perform the quantum-safe key encapsulation using the public key
                ciphertext, shared_secret = kem.encap_secret(public_key)
                # Encrypt the AES key using the shared secret from the Kyber encapsulation
                encrypted_aes_key = bytes(a ^ b for a, b in zip(aes_key, shared_secret))

                logger.info("AES key successfully encrypted using quantum-safe Kyber public key.")
                return ciphertext, encrypted_aes_key
        except Exception as e:
            logger.error(f"Error encrypting AES key with Kyber: {str(e)}", exc_info=True)
            return None, None

    def decrypt_aes_key_with_kyber(self, encrypted_aes_key, key_name, kms_aes_key_name):
        """
        Decrypt the AES key using a quantum-safe Kyber private key.
        :param encrypted_aes_key: The encrypted AES key to decrypt (in bytes).
        :param key_name: The KMS key resource name for retrieving the Kyber private key.
        :param kms_aes_key_name: The KMS key resource name used to decrypt the AES key.
        :return: The decrypted AES key (in bytes), or None on failure.
        """
        try:
            # Load the Kyber private key from key management
            _, private_key = load_key_pair_from_kms(key_name, kms_aes_key_name)

            if not private_key:
                raise ValueError("Failed to retrieve Kyber private key.")

            with oqs.KeyEncapsulation('Kyber768') as kem:
                aes_key = kem.decap_secret(encrypted_aes_key, private_key)
                logger.info("AES key successfully decrypted using quantum-safe Kyber private key.")
                return aes_key
        except Exception as e:
            logger.error(f"Error decrypting AES key with Kyber: {str(e)}", exc_info=True)
            return None

    # Message Signing and Verification with Dilithium

    def sign_message_with_dilithium(self, message, key_name, kms_aes_key_name):
        """
        Sign a message using a quantum-safe Dilithium private key.
        :param message: The message to sign (in bytes).
        :param key_name: The KMS key resource name for retrieving the Dilithium private key.
        :param kms_aes_key_name: The KMS key resource name used to decrypt the AES key.
        :return: The signature (in bytes), or None on failure.
        """
        try:
            # Load the Dilithium private key from key management
            _, private_key = load_key_pair_from_kms(key_name, kms_aes_key_name)

            if not private_key:
                raise ValueError("Failed to retrieve Dilithium private key.")

            with oqs.Signature('Dilithium3') as signer:
                signature = signer.sign(message, private_key)
                logger.info("Message successfully signed using Dilithium.")
                return signature
        except Exception as e:
            logger.error(f"Error signing message with Dilithium: {str(e)}", exc_info=True)
            return None

    def verify_dilithium_signature(self, message, signature, key_name, kms_aes_key_name):
        """
        Verify a signature using a quantum-safe Dilithium public key.
        :param message: The original message (in bytes).
        :param signature: The signature to verify (in bytes).
        :param key_name: The KMS key resource name for retrieving the Dilithium public key.
        :param kms_aes_key_name: The KMS key resource name used to decrypt the AES key.
        :return: True if the signature is valid, False otherwise.
        """
        try:
            # Load the Dilithium public key from key management
            public_key, _ = load_key_pair_from_kms(key_name, kms_aes_key_name)

            if not public_key:
                raise ValueError("Failed to retrieve Dilithium public key.")

            with oqs.Signature('Dilithium3') as verifier:
                valid = verifier.verify(message, signature, public_key)
                if valid:
                    logger.info("Dilithium signature is valid.")
                else:
                    logger.warning("Dilithium signature verification failed.")
                return valid
        except Exception as e:
            logger.error(f"Error verifying Dilithium signature: {str(e)}", exc_info=True)
            return False
