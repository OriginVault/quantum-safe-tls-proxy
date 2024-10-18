import asyncio
from utils.logger import get_logger
from tls_setup import create_tls_context

logger = get_logger(__name__)

class QuantumSafeProxy:
    def __init__(self, host, port, backend_host, backend_port, cert_file, key_file, ca_file=None):
        """
        Initializes the quantum-safe proxy.
        
        Args:
            host (str): Host address for the proxy to listen on.
            port (int): Port number for the proxy to listen on.
            backend_host (str): Host address for the backend server.
            backend_port (int): Port number for the backend server.
            cert_file (str): Path to the TLS certificate file.
            key_file (str): Path to the private key file.
            ca_file (str, optional): Path to the CA certificate file.
        """
        self.host = host
        self.port = port
        self.backend_host = backend_host
        self.backend_port = backend_port
        self.tls_context = create_tls_context(cert_file, key_file, ca_file)

    async def handle_client(self, reader, writer):
        """
        Handles incoming client connections and forwards them to the backend.
        
        Args:
            reader (asyncio.StreamReader): Reader for client input.
            writer (asyncio.StreamWriter): Writer for sending responses.
        """
        peername = writer.get_extra_info('peername')
        logger.info(f"Accepted connection from {peername}")

        try:
            backend_reader, backend_writer = await asyncio.open_connection(
                self.backend_host, self.backend_port, ssl=self.tls_context
            )

            async def forward_data(src_reader, dst_writer):
                try:
                    while True:
                        data = await src_reader.read(4096)
                        if not data:
                            break
                        dst_writer.write(data)
                        await dst_writer.drain()
                except Exception as e:
                    logger.warning(f"Error during data forwarding: {e}")
                finally:
                    dst_writer.close()

            await asyncio.gather(
                forward_data(reader, backend_writer),
                forward_data(backend_reader, writer)
            )
        except Exception as e:
            logger.error(f"Error handling client {peername}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f"Connection with {peername} closed.")

    async def start(self):
        """
        Starts the quantum-safe TLS proxy server.
        """
        server = await asyncio.start_server(self.handle_client, self.host, self.port, ssl=self.tls_context)
        logger.info(f"Quantum-safe TLS proxy running on {self.host}:{self.port}")
        
        try:
            async with server:
                await server.serve_forever()
        except asyncio.CancelledError:
            logger.info("Server shutdown initiated.")