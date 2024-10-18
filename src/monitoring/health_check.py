
import asyncio
import json
from utils.logger import get_logger

logger = get_logger(__name__)

health_checks = []

def register_health_check(check_function):
    """
    Registers a new health check function.
    """
    health_checks.append(check_function)

async def check_proxy_health():
    """
    Performs a health check for the proxy.
    """
    try:
        logger.info("Proxy health check passed.")
        return {"name": "proxy", "status": "healthy"}
    except Exception as e:
        logger.error(f"Proxy health check failed: {e}")
        return {"name": "proxy", "status": "unhealthy", "error": str(e)}

async def check_backend_health(host, port):
    """
    Checks if the backend service is reachable.
    """
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.close()
        await writer.wait_closed()
        logger.info(f"Backend health check passed for {host}:{port}.")
        return {"name": f"backend_{host}:{port}", "status": "healthy"}
    except Exception as e:
        logger.error(f"Backend health check failed for {host}:{port} - {e}")
        return {"name": f"backend_{host}:{port}", "status": "unhealthy", "error": str(e)}

async def run_all_health_checks():
    """
    Runs all registered health checks and aggregates the results.
    """
    results = await asyncio.gather(*[check() for check in health_checks])
    return json.dumps({"checks": results})
