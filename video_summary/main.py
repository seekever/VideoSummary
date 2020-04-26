""" The main module of the app."""

import logging
import sys

from PyQt5.QtWidgets import QApplication

from video_summary.models.general_options_model import GeneralOptions
from video_summary.models.main_window_model import MainWindow
from video_summary.models.objects_options_model import ObjectsOptions

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

    # Windows
    main_window = MainWindow()
    general_options = GeneralOptions()
    objects_options = ObjectsOptions()

    # Signals
    main_window.next.connect(lambda: load_window(general_options))
    general_options.previous.connect(lambda: load_window(main_window))
    general_options.next.connect(lambda: load_window(objects_options))
    objects_options.previous.connect(lambda: load_window(general_options))

    load_window(main_window)

    app.exec_()
    LOG.info('ending app')


if __name__ == '__main__':
    main()
