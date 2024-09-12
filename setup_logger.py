import logging
import os

    

def get_logger(file_object: __file__):


    LOGS_DIRECTORY = 'logs'
    os.makedirs(LOGS_DIRECTORY, exist_ok=True)

    file_name = os.path.splitext(os.path.basename(file_object))[0]


    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler for writing logs
    file_handler = logging.FileHandler(f'logs/{file_name}.log', encoding='utf-8')

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    # Test logger
#    logger.debug("Logger {file_name} is working!")

    return logger