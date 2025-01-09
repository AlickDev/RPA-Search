import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


class SafeTimedRotatingFileHandler(TimedRotatingFileHandler):
    def emit(self, record):
        if not os.path.exists(self.baseFilename):
            self.stream = self._open()
        super().emit(record)


def create_logger(log_folder="logs"):
    # Ensure the log folder exists
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Define the log file path without adding the date
    log_file_path = os.path.join(log_folder, 'elasticsearch.log')

    # Create or get a logger
    logger = logging.getLogger("AppLogger")

    # Avoid duplicate handlers
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Create the custom file handler
        file_handler = SafeTimedRotatingFileHandler(
            log_file_path, when="midnight", interval=1, backupCount=90, encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)

        # Set formatter for the handler
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger

