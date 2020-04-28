""" The module for the resume window."""

import logging
import os

# Paths
from PyQt5 import QtWidgets, uic

from video_summary.models.model_interface import ModelInterface

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'ResumeWindow.ui')

# Window
WINDOW_TITLE = "Resume window"

# Logger
LOGGER_NAME = 'App.Models.ResumeWindow'
LOG = logging.getLogger(LOGGER_NAME)


class ResumeWindow(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the resume window.

    ...

    Methods
    -------
    update_scenes_analysis_progress_bar(value)
        update the progress bar of the scenes analysis
    update_objects_analysis_progress_bar(value)
        update the progress bar of the objects analysis
    update_subtitles_analysis_progress_bar(value)
        update the progress bar of the subtitles analysis
    update_resume_progress_bar(value)
        update the progress bar of the resume
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)

        self.update_scenes_analysis_progress_bar(0)
        self.update_objects_analysis_progress_bar(0)
        self.update_subtitles_analysis_progress_bar(0)
        self.update_resume_progress_bar(0)

    def update_scenes_analysis_progress_bar(self, value):
        """
        Method that update the progress bar of the scenes analysis.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating scenes analysis progress bar')
        self.sceneAnalysisBar.setValue(value)
        LOG.debug('scenes analysis progress bar updated: %s / 100', value)

    def update_objects_analysis_progress_bar(self, value):
        """
        Method that update the progress bar of the objects analysis.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating objects analysis progress bar')
        self.objectAnalysisBar.setValue(value)
        LOG.debug('objects analysis progress bar updated: %s / 100', value)

    def update_subtitles_analysis_progress_bar(self, value):
        """
        Method that update the progress bar of the subtitles analysis.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating subtitles analysis progress bar')
        self.subtitleAnalysisBar.setValue(value)
        LOG.debug('subtitles analysis progress bar updated: %s / 100', value)

    def update_resume_progress_bar(self, value):
        """
        Method that update the progress bar of the resume.

        Parameters
        ----------
        value : int
            the progress bar value (0 - 100)
        """

        LOG.debug('updating resume progress bar')
        self.resumeBar.setValue(value)
        LOG.debug('resume progress bar updated: %s / 100', value)
