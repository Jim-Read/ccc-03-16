import os
import logging
from logging.handlers import TimedRotatingFileHandler

log_dir = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_handler = TimedRotatingFileHandler(os.path.join(log_dir, '_current.log'), when="midnight")
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)