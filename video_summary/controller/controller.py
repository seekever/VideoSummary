"""The window controller for the app."""

import logging
import sys

from PyQt5.QtWidgets import QApplication

from video_summary.context.general_context import GeneralContext, ResumeMode
from video_summary.models.general_options_model import GeneralOptions
from video_summary.models.main_window_model import MainWindow
from video_summary.models.objects_options_model import ObjectsOptions
from video_summary.models.resume_options_model import ResumeOptions
from video_summary.models.resume_result_model import ResumeResult
from video_summary.models.resume_window_model import ResumeWindow
from video_summary.models.subtitles_options_model import SubtitlesOptions

# Logger
LOGGER_NAME = 'App.Controller'
LOG = logging.getLogger(LOGGER_NAME)


def load_window(window):
    """ Method that prepare and show a window."""
    LOG.debug("preparing window")
    window.load_context()
    window.reload_conditional_format()
    window.show()


class Controller:
    """
    The class for the window's controller.

    ...

    Methods
    -------
    general_options_next()
        redirect to the general option's next window
    objects_options_next()
        redirect to the objects option's next window
    subtitles_options_previous()
        redirect to the subtitles option's previous window
    resume_options_previous ()
        redirect to the general option's previous window

    """

    def __init__(self):
        LOG.info('starting app')
        app = QApplication(sys.argv)

        # Windows
        self.main_window = MainWindow()
        self.general_options = GeneralOptions()
        self.objects_options = ObjectsOptions()
        self.subtitles_options = SubtitlesOptions()
        self.resume_options = ResumeOptions()
        self.resume_window = ResumeWindow()
        self.resume_result = ResumeResult()

        # Signals
        self.main_window.next.connect(lambda: load_window(self.general_options))
        self.general_options.previous.connect(lambda: load_window(self.main_window))
        self.general_options.next.connect(self.general_options_next)
        self.objects_options.previous.connect(lambda: load_window(self.general_options))
        self.objects_options.next.connect(self.objects_options_next)
        self.subtitles_options.previous.connect(self.subtitles_options_previous)
        self.subtitles_options.next.connect(lambda: load_window(self.resume_options))
        self.resume_options.previous.connect(self.resume_options_previous)
        self.resume_options.next.connect(lambda: load_window(self.resume_window))
        self.resume_window.previous.connect(lambda: load_window(self.resume_options))
        self.resume_window.next.connect(lambda: load_window(self.resume_result))
        self.resume_result.next.connect(lambda: load_window(self.main_window))

        load_window(self.main_window)

        app.exec_()
        LOG.info('ending app')

    def general_options_next(self):
        """Method that redirect to the general option's next window"""
        LOG.debug('looking for general options next window')
        with GeneralContext(read_only=True) as manager:
            if manager.resume_mode == ResumeMode.SUBTITLES:
                LOG.info('redirecting from general options to subtitles options')
                load_window(self.subtitles_options)
            else:
                LOG.info('redirecting from general options to objects options')
                load_window(self.objects_options)

    def objects_options_next(self):
        """Method that redirect to the objects option's next window"""
        LOG.debug('looking for objects options next window')
        with GeneralContext(read_only=True) as manager:
            if manager.resume_mode == ResumeMode.SUBTITLES_AND_OBJECTS:
                LOG.info('redirecting from objects options to subtitles options')
                load_window(self.subtitles_options)
            else:
                LOG.info('redirecting from objects options to resume options')
                load_window(self.resume_options)

    def subtitles_options_previous(self):
        """Method that redirect to the subtitles option's previous window"""
        LOG.debug('looking for subtitles options previous window')
        with GeneralContext(read_only=True) as manager:
            if manager.resume_mode == ResumeMode.SUBTITLES_AND_OBJECTS:
                LOG.info('redirecting from subtitles options to objects options')
                load_window(self.objects_options)
            else:
                LOG.info('redirecting from subtitles options to general options')
                load_window(self.general_options)

    def resume_options_previous(self):
        """Method that redirect to the general option's previous window"""
        LOG.debug('looking for resume options previous window')
        with GeneralContext(read_only=True) as manager:
            if manager.resume_mode == ResumeMode.OBJECTS:
                LOG.info('redirecting from resume options to objects options')
                load_window(self.objects_options)
            else:
                LOG.info('redirecting from resume options to subtitles options')
                load_window(self.subtitles_options)
