""" The module for the resume options window."""
import json
import logging
import os

from PyQt5 import QtWidgets, uic

from video_summary.context.general_context import GeneralContext
from video_summary.context.objects_context import ObjectsContext
from video_summary.context.scenes_context import ScenesContext
from video_summary.context.subtitles_context import SubtitlesContext
from video_summary.controller.threads_controller import ThreadsController
from video_summary.models.model_interface import ModelInterface

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(ROOT_DIR, '../templates/', 'ResumeOptions.ui')

# Window
WINDOW_TITLE = "Resume options"

# Logger
LOGGER_NAME = 'App.Models.ResumeOptions'
LOG = logging.getLogger(LOGGER_NAME)


class ResumeOptions(QtWidgets.QMainWindow, ModelInterface):
    """
    The class for the resume options window.

    ...

    Attributes
    ----------
    configurations : dict
        the dict with all the context configs

    """

    # Context config
    configurations = dict()

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing resume options window model')
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

        self.update_scenes_analysis_progress_bar(0)
        self.update_objects_analysis_progress_bar(0)
        self.update_subtitles_analysis_progress_bar(0)
        LOG.info('resume options window model initialized')

    def load_context(self):
        LOG.debug('loading contexts')
        with GeneralContext(read_only=True) as manager:
            self.configurations["General"] = manager.config
        with ScenesContext(read_only=True) as manager:
            self.configurations["Subtitles"] = manager.config
        with ObjectsContext(read_only=True) as manager:
            self.configurations["Objects"] = manager.config
        with SubtitlesContext(read_only=True) as manager:
            self.configurations["Subtitles"] = manager.config

        self.resumeOptionsLabel.setText(json.dumps(self.configurations, indent=4))

        LOG.debug('contexts loaded')

    def next_window(self):
        super().next_window()
        if ThreadsController.resume_thread.isRunning():
            LOG.info('restarting resume thread')
            ThreadsController.resume_thread.restart_thread()
        else:
            LOG.info('starting resume thread')
            ThreadsController.resume_thread.start()
