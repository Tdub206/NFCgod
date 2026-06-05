"""
Centralized logging configuration for the fraud suite.
"""

import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(log_dir="logs", level=logging.INFO):
    """
    Configure centralized logging for all modules.
    
    Args:
        log_dir: Directory to store log files
        level: Logging level (default INFO)
    """
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler for all logs
    all_log_file = os.path.join(log_dir, 'fraud_suite.log')
    file_handler = logging.handlers.RotatingFileHandler(
        all_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # File handler for errors only
    error_log_file = os.path.join(log_dir, 'fraud_suite_errors.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=10*1024*1024,
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    logger.addHandler(error_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"Logging initialized. Log directory: {log_dir}")
    return logger


def get_logger(name):
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)
