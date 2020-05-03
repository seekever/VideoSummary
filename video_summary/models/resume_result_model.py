""" The module for the resume result window."""

import logging
import os

from PyQt5 import QtWidgets, uic

from video_summary.models.model_interface import ModelInterface

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'ResumeResult.ui')

# Window
WINDOW_TITLE = "Resume result"

# Logger
LOGGER_NAME = 'App.Models.ResumeResult'
LOG = logging.getLogger(LOGGER_NAME)


class ResumeResult(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the resume result window.

    ...

    Methods
    -------
    download_video()
        downloads the final video

    """

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing resume result window model')
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.downloadButton.clicked.connect(self.download_video)
        self.restartButton.clicked.connect(self.next_window)
        LOG.info('resume result window model initialized')

    def download_video(self):
        """ Method that downloads the final video."""
        LOG.debug('downloadButton clicked')
        # TODO
