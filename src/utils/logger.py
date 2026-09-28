import logging
import sys
from pathlib import Path

from src.config.config import get_config


def setup_logger(name: str = "norvi") -> logging.Logger:
    """
    Configures and returns a logger instance based on the application configuration.
    """
    config = get_config()
    
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if setup is called multiple times
    if logger.hasHandlers():
        return logger

    # Map string log level to logging module constant
    log_level_str = config.log_level.upper()
    level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_dir = Path(config.app_data_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Create a default logger instance
logger = setup_logger()
