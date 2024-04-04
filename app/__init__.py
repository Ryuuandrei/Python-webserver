from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

import logging
from logging.handlers import RotatingFileHandler
import time

webserver = Flask(__name__)

webserver.logger = logging.getLogger('webserver')
webserver.logger.setLevel(logging.INFO)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                               datefmt='%Y-%m-%d %H:%M:%S')

log_format.converter = time.gmtime

log_file = 'webserver.log'
log_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
log_handler.setFormatter(log_format)
webserver.logger.addHandler(log_handler)

webserver.logger.info(f'Start server')

webserver.tasks_runner = ThreadPool([])

# webserver.task_runner.start()
webserver.shutdown = False
webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

from app import routes
