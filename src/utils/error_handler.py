from utils.logger import get_logger
import traceback

# Get the centralized logger instance
logger = get_logger(__name__)

def log_error(error_message, exception=None, extra_context=None):
    """
    Logs an error message with optional exception details and extra context.
    
    Args:
        error_message (str): The main error message to log.
        exception (Exception, optional): The exception instance (if available).
        extra_context (dict, optional): Additional context information to log.
    """
    # Create the base log message
    log_message = f"Error: {error_message}"

    # Append exception details if available
    if exception is not None:
        log_message += f" | Exception: {str(exception)}"
        # Add the traceback to the log if available
        traceback_details = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        log_message += f"\nTraceback:\n{traceback_details}"

    # Append extra context if provided
    if extra_context:
        log_message += f" | Context: {extra_context}"

    # Use the centralized logger to log the error message
    logger.error(log_message)

def handle_exception(exception, context_message=None):
    """
    Handles an exception by logging it and optionally raising it again.
    
    Args:
        exception (Exception): The exception instance to handle.
        context_message (str, optional): Additional context to include in the log.
    
    Raises:
        Exception: Re-raises the original exception after logging.
    """
    # Log the error with an optional context message
    if context_message:
        log_error(context_message, exception=exception)
    else:
        log_error("An exception occurred", exception=exception)

    # Optionally, raise the exception again if needed
    raise exception

def safe_execute(function, *args, **kwargs):
    """
    Executes a function safely, catching and logging any exceptions.
    
    Args:
        function (callable): The function to execute.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
    
    Returns:
        The result of the function if successful, None otherwise.
    """
    try:
        return function(*args, **kwargs)
    except Exception as e:
        log_error("Error during function execution", exception=e, extra_context={"function": function.__name__})
        return None
