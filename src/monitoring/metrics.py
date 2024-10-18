
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from utils.logger import get_logger

logger = get_logger(__name__)

# Define custom Prometheus metrics
REQUEST_COUNTER = Counter('proxy_requests_total', 'Total number of requests received')
RATE_LIMITED_COUNTER = Counter('proxy_rate_limited_total', 'Total number of rate-limited requests')
ERROR_COUNTER = Counter('proxy_errors_total', 'Total number of errors encountered')
REQUEST_LATENCY = Histogram('proxy_request_latency_seconds', 'Histogram of request latency')
ACTIVE_CONNECTIONS = Gauge('proxy_active_connections', 'Current number of active connections')

def start_metrics_server(port=9090):
    """
    Starts the Prometheus metrics server.
    """
    start_http_server(port)
    logger.info(f"Prometheus metrics server started on port {port}")

def increment_request_counter():
    """
    Increments the request counter.
    """
    REQUEST_COUNTER.inc()

def increment_rate_limited_counter():
    """
    Increments the rate-limited request counter.
    """
    RATE_LIMITED_COUNTER.inc()

def increment_error_counter():
    """
    Increments the error counter.
    """
    ERROR_COUNTER.inc()

def observe_request_latency(seconds):
    """
    Observes the latency of a request.
    """
    REQUEST_LATENCY.observe(seconds)

def set_active_connections(count):
    """
    Sets the current number of active connections.
    """
    ACTIVE_CONNECTIONS.set(count)
