import sys
import logging


def get_logger(logger_name, is_debug, log_file):
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    custom_logger = logging.getLogger(logger_name)
    if is_debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=log_format)
    else:
        logging.basicConfig(filename=log_file, level=logging.INFO, format=log_format)
        logging.getLogger('asyncio').setLevel(logging.WARNING)  # Suppress Asyncio info logs
    return custom_logger
