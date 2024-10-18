import os
import json
import yaml
from utils.logger import get_logger

logger = get_logger(__name__)

class ConfigLoader:
    """
    Loads and manages configuration settings for the application.
    """

    def __init__(self, config_file=None, env_prefix="APP_"):
        """
        Initializes the ConfigLoader.
        
        Args:
            config_file (str, optional): Path to the configuration file (JSON or YAML).
            env_prefix (str, optional): Prefix for environment variables (default is "APP_").
        """
        self.config_file = config_file
        self.env_prefix = env_prefix
        self.config = {}

        # Load configurations from the file and environment
        self.load_config()

    def load_config(self):
        """
        Loads the configuration from the specified file and environment variables.
        """
        if self.config_file:
            self.load_from_file(self.config_file)

        self.load_from_env()

    def load_from_file(self, file_path):
        """
        Loads configuration from a JSON or YAML file.
        
        Args:
            file_path (str): Path to the configuration file.
        """
        try:
            with open(file_path, 'r') as file:
                if file_path.endswith(".json"):
                    self.config.update(json.load(file))
                elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
                    self.config.update(yaml.safe_load(file))
                else:
                    logger.error(f"Unsupported file format: {file_path}")
                    return
            logger.info(f"Configuration loaded from file: {file_path}")
        except Exception as e:
            logger.error(f"Failed to load configuration from file {file_path}: {e}")

    def load_from_env(self):
        """
        Loads configuration from environment variables with the specified prefix.
        """
        for key, value in os.environ.items():
            if key.startswith(self.env_prefix):
                # Remove the prefix and use the rest of the key as the configuration key
                config_key = key[len(self.env_prefix):]
                self.config[config_key] = value
        logger.info("Configuration loaded from environment variables.")

    def get(self, key, default=None):
        """
        Retrieves a configuration value.
        
        Args:
            key (str): The configuration key.
            default: The default value if the key is not found (default is None).
        
        Returns:
            The configuration value or the default if not found.
        """
        return self.config.get(key, default)

    def get_all(self):
        """
        Returns all configuration settings.
        
        Returns:
            dict: The entire configuration dictionary.
        """
        return self.config
