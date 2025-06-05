import sys
import traceback
from src.logger import setup_logger

# Initialize logger
logger = setup_logger()

class ProjectException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _, _, exec_tb = error_details.exc_info()

        self.lineno = exec_tb.tb_lineno
        self.filename = exec_tb.tb_frame.f_code.co_filename

    def __str__(self):
        logger.info("Exception raised: ")
        details = f'\nError occured in file: {self.filename}, \nline: {self.lineno}, \nError Msg: {self.error_message}'
        logger.info(details)
        return details