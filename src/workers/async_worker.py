import asyncio
from utils.logger import get_logger

logger = get_logger(__name__)

class AsyncWorker:
    """
    A worker for performing background tasks asynchronously, such as certificate renewal and TLS reload.
    """

    def __init__(self, cert_manager, tls_service, check_interval=3600):
        """
        Initializes the AsyncWorker.
        
        Args:
            cert_manager (CertificateManager): The certificate manager instance.
            tls_service (TLSService): The TLS service instance.
            check_interval (int): Interval in seconds between each certificate check.
        """
        self.cert_manager = cert_manager
        self.tls_service = tls_service
        self.check_interval = check_interval
        self.running = False

    async def start(self):
        """
        Starts the async worker to periodically perform tasks.
        """
        self.running = True
        logger.info("Async worker started.")
        while self.running:
            await self.run_tasks()
            await asyncio.sleep(self.check_interval)

    async def run_tasks(self):
        """
        Runs the background tasks, such as certificate validation and renewal.
        """
        try:
            logger.info("Running background tasks.")
            # Check if the certificate needs renewal
            if not self.cert_manager.validate_certificate():
                logger.info("Certificate is near expiration or invalid. Attempting renewal.")
                # Attempt certificate renewal
                if self.cert_manager.renew_certificate():
                    logger.info("Certificate renewed successfully. Reloading TLS context.")
                    # Reload the TLS context after renewal
                    self.tls_service._setup_tls_context()
                else:
                    logger.error("Certificate renewal failed.")
            else:
                logger.info("Certificate is valid. No renewal needed.")
        except Exception as e:
            logger.error(f"Error while running background tasks: {e}")

    async def stop(self):
        """
        Stops the async worker.
        """
        self.running = False
        logger.info("Async worker stopped.")
