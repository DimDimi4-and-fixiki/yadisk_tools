import logging


class Logger:
    def __init__(self, module_name, log_file_path=None, level=logging.DEBUG):

        # Initialize logger and set logging level
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(level)

        # If file for logging was specified
        if log_file_path is not None:

            # Define file handler for logger
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)

            # Add file handler to the logger config
            self.logger.addHandler(file_handler)

        # Define stream handler for logger
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_formatter = logging.Formatter('%(asctime)s - %(levelname)s: ------ %(message)s ------')
        stream_handler.setFormatter(stream_formatter)

        # Add stream handler to the logger config
        self.logger.addHandler(stream_handler)

    def log(self, msg: str, level: str = 'debug'):

        logging_functions = {
            'debug': self.logger.debug,
            'info': self.logger.info,
            'error': self.logger.error,
            'critical': self.logger.critical,
            'exception': self.logger.exception
        }

        level = level.lower()
        if level in logging_functions:
            logging_function = logging_functions[level]
            logging_function(msg)
