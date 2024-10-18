import jwt
from utils.logger import get_logger

logger = get_logger(__name__)

class AuthHandler:
    """
    Handles authentication for incoming requests using JWT tokens.
    """

    def __init__(self, secret_key, algorithm="HS256"):
        """
        Initializes the AuthHandler.
        
        Args:
            secret_key (str): The secret key used to decode JWT tokens.
            algorithm (str): The algorithm used for JWT encoding/decoding (default: HS256).
        """
        self.secret_key = secret_key
        self.algorithm = algorithm

    def validate_token(self, token):
        """
        Validates a JWT token.
        
        Args:
            token (str): The JWT token to validate.
        
        Returns:
            dict: Decoded token data if valid, None otherwise.
        """
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            logger.info("Authentication successful: JWT token is valid.")
            return decoded_token
        except jwt.ExpiredSignatureError:
            logger.warning("Authentication failed: Token has expired.")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Authentication failed: Invalid token.")
            return None

    def authenticate_request(self, headers):
        """
        Authenticates a request based on the JWT token in the Authorization header.
        
        Args:
            headers (dict): Request headers.
        
        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        auth_header = headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("Authentication failed: Missing or invalid Authorization header.")
            return False

        token = auth_header.split("Bearer ")[1]
        return self.validate_token(token) is not None
