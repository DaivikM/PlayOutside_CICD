import logging
import os
from datetime import datetime

def setup_logger(log_dir="logs"):
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Generate unique log filename based on current datetime
    log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
    log_path = os.path.join(log_dir, log_filename)

    # Create logger
    logger = logging.getLogger("PredictionLogger")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        # Create file handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(file_handler)

    return logger
