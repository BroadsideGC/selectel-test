import logging
import os

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
LOG_LEVEL = os.getenv('LOG_LEVEL', logging.INFO)