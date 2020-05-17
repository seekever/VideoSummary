""" The module for the resume window."""

import logging
import os

# Paths
from PyQt5 import QtWidgets, uic

from video_summary.controller.threads_controller import ThreadsController
from video_summary.models.model_interface import ModelInterface

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'ResumeWindow.ui')

# Window
WINDOW_TITLE = "Resume window"

# Logger
LOGGER_NAME = 'App.Models.ResumeWindow'
LOG = logging.getLogger(LOGGER_NAME)


class ResumeWindow(QtWidgets.QMainWindow, ModelInterface):
    """The class for the resume window."""

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing resume window model')
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)

        ThreadsController.scenes_analysis_thread.progress.connect(
            self.update_scenes_analysis_progress_bar)
        ThreadsController.objects_analysis_thread.progress.connect(
            self.update_objects_analysis_progress_bar)
        ThreadsController.subtitles_analysis_thread.progress.connect(
            self.update_subtitles_analysis_progress_bar)
        ThreadsController.resume_thread.progress.connect(
            self.update_resume_progress_bar)

        self.update_scenes_analysis_progress_bar(0)
        self.update_objects_analysis_progress_bar(0)
        self.update_subtitles_analysis_progress_bar(0)
        self.update_resume_progress_bar(0)
        LOG.info('resume window model initialized')

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.nextButton.setVisible(self.resumeBar.value() == 100)
        LOG.debug('conditional format reloaded')

    def update_resume_progress_bar(self, value):
        super().update_resume_progress_bar(value)
        if value == 100:
            self.reload_conditional_format()
