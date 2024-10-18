import logging
import logging.config
import os
import json

def setup_logger(log_level=logging.INFO, log_to_file=True, log_file='logs/app.log', log_format='plain', max_bytes=5*1024*1024, backup_count=3):
    """
    Sets up a centralized logger for the application.
    
    Args:
        log_level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
        log_to_file (bool): Whether to log to a file or just to the console.
        log_file (str): The log file path, if logging to a file.
        log_format (str): The log format ('plain' for text, 'json' for JSON).
        max_bytes (int): Maximum size of log file before rotation (in bytes).
        backup_count (int): Number of backup log files to keep.
    """
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'plain': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': log_format,
                'level': log_level
            }
        },
        'root': {
            'handlers': ['console'],
            'level': log_level
        }
    }
    
    if log_to_file:
        # Ensure the logs directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Add file handler with rotation
        log_config['handlers']['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': log_format,
            'level': log_level,
            'filename': log_file,
            'maxBytes': max_bytes,
            'backupCount': backup_count
        }
        log_config['root']['handlers'].append('file')
    
    # Configure logging
    logging.config.dictConfig(log_config)
    logging.info("Logger configured successfully with level: %s", logging.getLevelName(log_level))

def get_logger(name):
    """
    Gets a logger with the specified name.
    
    Args:
        name (str): The name of the logger.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
