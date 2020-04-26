""" The main module of the app."""

import logging
import sys

from PyQt5.QtWidgets import QApplication

from video_summary.models.main_window_model import MainWindow

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


def load_window(window):
    """ Method that prepare and show a window."""
    window.load_context()
    window.reload_conditional_format()
    window.show()


def main():
    """ Method that controls the application."""
    LOG.info('starting app')
    app = QApplication(sys.argv)

    main_window = MainWindow()
    load_window(main_window)

    app.exec_()
    LOG.info('ending app')


if __name__ == '__main__':
    main()
