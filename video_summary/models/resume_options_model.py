""" The module for the resume options window."""

import logging
import os

from PyQt5 import QtWidgets, uic

from video_summary import utils
from video_summary.context.general_context import GeneralContext, ResumeMode
from video_summary.context.objects_context import ObjectsContext
from video_summary.context.subtitles_context import SubtitlesContext
from video_summary.controller.processes_controller import ProcessesController
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
    detect_scenes : bool
        a boolean to activate the detect scenes' progress bar
    object_analysis : bool
        a boolean to activate the object analysis' progress bar
    subtitle_analysis : bool
        a boolean to activate the subtitle analysis' progress bar

    """

    # Context config
    configurations = dict()

    # Progress bars visibility
    detect_scenes = True
    object_analysis = True
    subtitle_analysis = True

    def __init__(self, *args, **kwargs):
        LOG.debug('initializing resume options window model')
        super().__init__(*args, *kwargs)

        uic.loadUi(TEMPLATE_PATH, self)

        self.setWindowTitle(WINDOW_TITLE)

        self.previousButton.clicked.connect(self.previous_window)
        self.nextButton.clicked.connect(self.next_window)

        ProcessesController.scenes_analysis_process.progress.connect(
            self.update_scenes_analysis_progress_bar)
        ProcessesController.objects_analysis_process.progress.connect(
            self.update_objects_analysis_progress_bar)
        ProcessesController.subtitles_analysis_process.progress.connect(
            self.update_subtitles_analysis_progress_bar)

        self.update_scenes_analysis_progress_bar(0)
        self.update_objects_analysis_progress_bar(0)
        self.update_subtitles_analysis_progress_bar(0)
        LOG.info('resume options window model initialized')

    def load_context(self):
        LOG.debug('loading contexts')
        with GeneralContext(read_only=True) as manager:
            self.configurations["General"] = manager.config
            self.detect_scenes = manager.detect_scenes
            self.object_analysis = manager.resume_mode in (ResumeMode.OBJECTS,
                                                           ResumeMode.SUBTITLES_AND_OBJECTS)
            self.subtitle_analysis = manager.resume_mode in (ResumeMode.SUBTITLES,
                                                             ResumeMode.SUBTITLES_AND_OBJECTS)
        with ObjectsContext(read_only=True) as manager:
            self.configurations["Objects"] = manager.config
        with SubtitlesContext(read_only=True) as manager:
            self.configurations["Subtitles"] = manager.config

        self.resumeOptionsLabel.setText(utils.print_config(self.configurations))

        LOG.debug('contexts loaded')

    def reload_conditional_format(self):
        LOG.debug('reloading conditional format')
        self.scenesProgressWidget.setVisible(self.detect_scenes)
        self.objectsProgressWidget.setVisible(self.object_analysis)
        self.subtitlesProgressWidget.setVisible(self.subtitle_analysis)
        LOG.debug('conditional format reloaded')

    def next_window(self):
        super().next_window()
        if ProcessesController.resume_process.isRunning():
            LOG.info('restarting resume process')
            ProcessesController.resume_process.restart_process()
        else:
            LOG.info('starting resume process')
            ProcessesController.resume_process.start()
