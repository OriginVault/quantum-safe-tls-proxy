import aiohttp
import asyncio
from utils.logger import get_logger

logger = get_logger(__name__)

class BackendService:
 """
 Interacts with backend services, handling requests and responses.
 """

 def __init__(self, base_url, max_retries=3, timeout=10):
     """
     Initializes the BackendService.
     
     Args:
         base_url (str): The base URL of the backend service.
         max_retries (int): Maximum number of retries for a failed request.
         timeout (int): Timeout for the request in seconds.
     """
     self.base_url = base_url
     self.max_retries = max_retries
     self.timeout = timeout

 async def send_request(self, endpoint, method="GET", data=None, headers=None):
     """
     Sends a request to the backend service with retries.
     
     Args:
         endpoint (str): The API endpoint.
         method (str): HTTP method (default is "GET").
         data (dict, optional): The request payload.
         headers (dict, optional): Additional headers.
     
     Returns:
         dict: The response data.
     """
     url = f"{self.base_url}/{endpoint.lstrip('/')}"
     headers = headers or {}
     retries = 0

     while retries < self.max_retries:
         try:
             async with aiohttp.ClientSession() as session:
                 async with session.request(method, url, json=data, headers=headers, timeout=self.timeout) as response:
                     response_data = await response.json()
                     if response.status == 200:
                         logger.info(f"Request to {url} succeeded.")
                         return response_data
                     else:
                         logger.warning(f"Request to {url} failed with status {response.status}.")
                         retries += 1
                         await asyncio.sleep(2 ** retries)  # Exponential backoff
         except (aiohttp.ClientError, asyncio.TimeoutError) as e:
             logger.error(f"Error sending request to {url}: {e}")
             retries += 1
             await asyncio.sleep(2 ** retries)  # Exponential backoff
     
     raise Exception(f"Failed to complete request to {url} after {self.max_retries} retries")
