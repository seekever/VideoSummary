""" The main module of the app."""

import logging
import sys

from video_summary.controller.threads_controller import ThreadsController
from video_summary.controller.windows_controller import WindowsController

# Logger
LOGGER_NAME = 'App'
LOGGER_FILENAME = 'log.log'
LOGGER_LEVEL = logging.DEBUG
LOGGER_FORMAT = '%(asctime)s %(threadName)s %(levelname)-8s %(module)s: %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(filename=LOGGER_FILENAME, level=LOGGER_LEVEL,
                    format=LOGGER_FORMAT, datefmt=LOGGER_DATE_FORMAT)
logging.getLogger('PyQt5').setLevel(logging.WARNING)

LOG = logging.getLogger(LOGGER_NAME)
SH = logging.StreamHandler(sys.stdout)
SH.setFormatter(logging.Formatter(LOGGER_FORMAT))
LOG.addHandler(SH)

if __name__ == '__main__':
    WindowsController()
    ThreadsController()
