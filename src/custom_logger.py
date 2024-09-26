import inspect
import logging
import os

class Logger:
    
    def __init__(self):
        pass

    def log(self, message):
        caller = inspect.stack()[1]
        file_name = os.path.basename(caller.filename)
        caller_info = f"{file_name}:{caller.lineno}"
        logging.info(message)
        print(f"{caller_info} - {message}")