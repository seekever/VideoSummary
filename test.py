""" The main module of the app's tests."""

import logging
import sys
import unittest

from video_summary.test.contexts_test import ContextTest
from video_summary.test.utils_test import UtilsTest

# Logger
LOGGER_NAME = 'Test'
LOGGER_FILENAME = 'video_summary/test.log'
LOGGER_LEVEL = logging.DEBUG
LOGGER_FORMAT = '%(asctime)s %(threadName)s %(levelname)-8s %(module)s: %(message)s'
LOGGER_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(filename=LOGGER_FILENAME, level=LOGGER_LEVEL,
                    format=LOGGER_FORMAT, datefmt=LOGGER_DATE_FORMAT)
LOG = logging.getLogger(LOGGER_NAME)
SH = logging.StreamHandler(sys.stdout)
SH.setFormatter(logging.Formatter(LOGGER_FORMAT))
LOG.addHandler(SH)

if __name__ == '__main__':
    unittest.main()
    ContextTest()
    UtilsTest()
