import os
import boto3
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from utils.logger import get_logger

logger = get_logger(__name__)

def load_private_key(source, password=None):
    """
    Loads the private key from the specified source.
    
    Args:
        source (str): The source from which to load the private key (e.g., file path, secret manager).
        password (str, optional): Password for decrypting the private key.
    
    Returns:
        private_key: The loaded private key object.
    """
    if source.startswith("file://"):
        # Load from a file
        file_path = source.replace("file://", "")
        with open(file_path, "rb") as key_file:
            key_data = key_file.read()
            return load_pem_private_key(key_data, password=password)

    elif source.startswith("aws-secrets://"):
        # Load from AWS Secrets Manager
        secret_name = source.replace("aws-secrets://", "")
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=secret_name)
        key_data = response['SecretString'].encode()
        return load_pem_private_key(key_data, password=password)

    else:
        logger.error(f"Unsupported key source: {source}")
        raise ValueError("Unsupported key source")
