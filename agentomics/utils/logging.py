#! /usr/bin/env python3

"""Agentomics: Logging Utilities

Utilities to redirect standard output and warnings to a log file.

Author: Akhil Karra
"""

import logging
from logging.handlers import RotatingFileHandler


def configure_logging(log_level=logging.DEBUG, log_to_console=True, log_to_file=True, log_file="app.log", max_file_size=5*1024*1024, backup_count=3):
    """
    Configures logging with console and file handlers, with file rollover support.

    :param log_level: The logging level for the logger.
    :param log_to_console: Whether to log messages to the console.
    :param log_to_file: Whether to log messages to a file.
    :param log_file: The file to which logs should be written.
    :param max_file_size: Maximum size of the log file in bytes before rollover.
    :param backup_count: Number of backup log files to keep.
    """
    logger = logging.getLogger()
    logger.setLevel(log_level)  # Set the logging level based on the parameter

    # Formatter for log messages
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Clear existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add console handler
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)  # Set console logging level
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler with rollover
    if log_to_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count)
        file_handler.setLevel(log_level)  # Set file logging level
        file_handler.setFormatter(formatter)
        file_handler.doRollover()  # Force rotation on app start
        logger.addHandler(file_handler)

    logging.info("Logging configured: level=%s, console=%s, file=%s (max_size=%d bytes, backups=%d)",
                 logging.getLevelName(log_level), log_to_console, log_to_file, max_file_size, backup_count)


def main():
   configure_logging(log_to_console=True, log_to_file=True, log_file="app.log", max_file_size=2*1024*1024, backup_count=5)

   # Example log messages
   for i in range(10000):
       logging.debug(f"Debug message {i}")
       logging.info(f"Info message {i}")
       logging.warning(f"Warning message {i}")
       logging.error(f"Error message {i}")
       logging.critical(f"Critical message {i}")


if __name__ == "__main__":
    main()
