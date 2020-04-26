""" The module for the main window."""

import logging
import os

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from video_summary.context.general_context import GeneralContext
from video_summary.models.model_interface import ModelInterface

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'MainWindow.ui')

# Window
WINDOW_TITLE = "Main window"

# Logger
LOGGER_NAME = 'App.Models.MainWindow'
LOG = logging.getLogger(LOGGER_NAME)


class MainWindow(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the main window.

    ...

    Attributes
    ----------
    path : str
        the original video path

    Methods
    -------
    check_data()
        check if all context data is correct
    load_video()
        asks to the user the original video path
    """

    path = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.loadVideoButton.clicked.connect(self.load_video)
        self.nextButton.clicked.connect(self.next_window)

    def load_context(self):
        LOG.debug('loading context')
        with GeneralContext() as manager:
            self.path = manager.original_video_path
        LOG.debug('context loaded')

    def save_context(self):
        LOG.debug('saving context')
        with GeneralContext() as manager:
            manager.original_video_path = self.path
        LOG.debug('context saved')

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.nextButton.setVisible(self.check_data())
        LOG.debug('conditional format reloaded')

    def check_data(self):
        if self.path is None:
            return False
        if self.path == "":
            return False
        if not self.path.endswith('.mp4'):
            return False
        return True

    def load_video(self):
        """ Method that asks to the user the original video path."""
        LOG.debug('loadVideoButton clicked')

        LOG.debug('opening file dialog')
        self.path = QFileDialog.getOpenFileName(self, 'Load file', '',
                                                "Video files (*.mp4)").__getitem__(0)
        LOG.debug('file dialog closed')

        self.reload_conditional_format()
        LOG.info('original video path: %s', self.path)
