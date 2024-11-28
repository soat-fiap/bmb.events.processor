import inspect
import logging
import os
#import seqlog

#seqlog.configure_from_file('seq_config.yml')
class Logger:
    
    def __init__(self):
        pass

    def error(self, message):
        caller = inspect.stack()[1]
        file_name = os.path.basename(caller.filename)
        caller_info = f"{file_name}:{caller.lineno}"
        logging.error(message, extra={"caller_info": caller_info})

    def log(self, message):
        caller = inspect.stack()[1]
        file_name = os.path.basename(caller.filename)
        caller_info = f"{file_name}:{caller.lineno}"
        logging.info(message, extra={"caller_info": caller_info})
