import time
from collections import defaultdict
from utils.logger import get_logger

logger = get_logger(__name__)

class RateLimiter:
    """
    Implements a simple rate limiter using the token bucket algorithm.
    """

    def __init__(self, rate_limit=10, per_seconds=60):
        """
        Initializes the RateLimiter.
        
        Args:
            rate_limit (int): Maximum number of requests allowed within the time window.
            per_seconds (int): Time window in seconds.
        """
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.clients = defaultdict(lambda: {'tokens': rate_limit, 'last_time': time.time()})

    def is_allowed(self, client_id):
        """
        Checks if a request from a given client is allowed based on the rate limit.
        
        Args:
            client_id (str): The unique identifier for the client (e.g., IP address).
        
        Returns:
            bool: True if the request is allowed, False otherwise.
        """
        current_time = time.time()
        client_data = self.clients[client_id]

        # Refill tokens based on elapsed time
        elapsed_time = current_time - client_data['last_time']
        refill_tokens = int(elapsed_time * (self.rate_limit / self.per_seconds))
        client_data['tokens'] = min(self.rate_limit, client_data['tokens'] + refill_tokens)
        client_data['last_time'] = current_time

        # Check if tokens are available for this request
        if client_data['tokens'] > 0:
            client_data['tokens'] -= 1
            logger.info(f"Rate limiter: Request allowed for client {client_id}. Tokens left: {client_data['tokens']}")
            return True
        else:
            logger.warning(f"Rate limiter: Request denied for client {client_id}. Rate limit exceeded.")
            return False
