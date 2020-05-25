""" The module for the resume window."""

import logging
import os

# Paths
from PyQt5 import QtWidgets, uic

from video_summary.context.general_context import GeneralContext, ResumeMode
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
    """The class for the resume window.

    ...

    Attributes
    ----------
    detect_scenes : bool
        a boolean to activate the detect scenes' progress bar
    object_analysis : bool
        a boolean to activate the object analysis' progress bar
    subtitle_analysis : bool
        a boolean to activate the subtitle analysis' progress bar

    """

    # Progress bars visibility
    detect_scenes = True
    object_analysis = True
    subtitle_analysis = True

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

    def load_context(self):
        LOG.debug('loading contexts')
        with GeneralContext(read_only=True) as manager:
            self.detect_scenes = manager.detect_scenes
            self.object_analysis = manager.resume_mode in (ResumeMode.OBJECTS,
                                                           ResumeMode.SUBTITLES_AND_OBJECTS)
            self.subtitle_analysis = manager.resume_mode in (ResumeMode.SUBTITLES,
                                                             ResumeMode.SUBTITLES_AND_OBJECTS)
        LOG.debug('contexts loaded')

    def check_data(self):
        LOG.debug('checking data')
        with GeneralContext(read_only=True) as manager:
            if manager.resume_times is None:
                LOG.info('incorrect data (resume times is null)')
                return False
            if not manager.resume_times:
                LOG.info('incorrect data (resume times is empty)')
                return False
        LOG.info('checked data: OK')
        return True

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.scenesProgressWidget.setVisible(self.detect_scenes)
        self.objectsProgressWidget.setVisible(self.object_analysis)
        self.subtitlesProgressWidget.setVisible(self.subtitle_analysis)
        self.nextButton.setDisabled(self.resumeBar.value() != 100 or not self.check_data())
        LOG.debug('conditional format reloaded')

    def update_resume_progress_bar(self, value):
        super().update_resume_progress_bar(value)
        if value == 100:
            self.reload_conditional_format()
