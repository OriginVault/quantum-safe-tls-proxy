import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from google.cloud import kms_v1
from google.api_core import exceptions
from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize Google KMS client
kms_client = kms_v1.KeyManagementServiceClient()

def load_key_pair_from_kms(key_name, kms_aes_key_name, password=None):
    """
    Loads and decrypts a quantum key pair (public and private keys) stored in KMS.
    
    Args:
        key_name (str): The KMS key resource name where the encrypted key data is stored.
        kms_aes_key_name (str): The KMS key resource name used to decrypt the AES key.
        password (str, optional): Password for decrypting the private key, if required.
    
    Returns:
        tuple: A tuple containing the loaded public and private key objects.
    """
    try:
        # Step 1: Retrieve the encrypted key data from KMS
        encrypted_key_data = _retrieve_key_data_from_kms(key_name)

        # Step 2: Decrypt the AES key using KMS
        encrypted_aes_key = encrypted_key_data["encrypted_aes_key"]
        aes_key = _retrieve_aes_key_from_kms(encrypted_aes_key, kms_aes_key_name)

        # Step 3: Decrypt the key pair using the decrypted AES key
        encrypted_public_key = encrypted_key_data["encrypted_public_key"]
        encrypted_private_key = encrypted_key_data["encrypted_private_key"]

        decrypted_public_key_data = _decrypt_data_with_aes(encrypted_public_key, aes_key)
        decrypted_private_key_data = _decrypt_data_with_aes(encrypted_private_key, aes_key)

        # Step 4: Load the decrypted public and private keys
        public_key = load_pem_public_key(decrypted_public_key_data)
        private_key = load_pem_private_key(decrypted_private_key_data, password=password)

        logger.info(f"Key pair successfully decrypted and loaded from KMS key: {key_name}")
        return public_key, private_key

    except Exception as e:
        logger.error(f"Failed to load key pair from KMS. Error: {e}", exc_info=True)
        raise

def _retrieve_key_data_from_kms(key_name):
    """
    Retrieves the encrypted key data from KMS.
    
    Args:
        key_name (str): The KMS key resource name where the encrypted key data is stored.
    
    Returns:
        dict: The decrypted key data containing encrypted public/private keys and the AES key.
    """
    try:
        # Retrieve the encrypted key data from KMS
        response = kms_client.decrypt(request={"name": key_name, "ciphertext": b""})
        # Decode the response data as JSON
        key_data = json.loads(response.plaintext)
        logger.info(f"Key data retrieved successfully from KMS key: {key_name}")
        return key_data
    except exceptions.GoogleAPIError as e:
        logger.error(f"Failed to retrieve key data from KMS key: {key_name}. Error: {e}", exc_info=True)
        raise

def _retrieve_aes_key_from_kms(encrypted_aes_key, kms_key_name):
    """
    Decrypts the AES key using KMS.
    
    Args:
        encrypted_aes_key (bytes): The encrypted AES key.
        kms_key_name (str): The KMS key resource name for decryption.
    
    Returns:
        bytes: The decrypted AES key.
    """
    try:
        # Use the KMS client to decrypt the AES key
        response = kms_client.decrypt(request={"name": kms_key_name, "ciphertext": encrypted_aes_key})
        aes_key = response.plaintext
        logger.info(f"AES key decrypted successfully using KMS key: {kms_key_name}")
        return aes_key
    except exceptions.GoogleAPIError as e:
        logger.error(f"Failed to decrypt AES key using KMS key: {kms_key_name}. Error: {e}", exc_info=True)
        raise

def _decrypt_data_with_aes(encrypted_data, aes_key):
    """
    Decrypts data using the provided AES key.
    
    Args:
        encrypted_data (bytes): The data to decrypt.
        aes_key (bytes): The AES key used for decryption.
    
    Returns:
        bytes: The decrypted data.
    """
    try:
        iv = encrypted_data[:16]  # Extract the initialization vector (IV)
        actual_encrypted_data = encrypted_data[16:]  # The rest is the encrypted data

        # Create the Cipher object for AES decryption
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Perform the decryption and return the decrypted data
        decrypted_data = decryptor.update(actual_encrypted_data) + decryptor.finalize()
        logger.info("Data decrypted successfully with AES.")
        return decrypted_data

    except Exception as e:
        logger.error("Failed to decrypt data with AES.", exc_info=True)
        raise
