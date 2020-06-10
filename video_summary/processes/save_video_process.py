""" The module for the save video process."""

import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QObject
from moviepy.video.compositing.concatenate import concatenate_videoclips
from proglog import TqdmProgressBarLogger

from video_summary.context.general_context import GeneralContext
from video_summary.utils import load_video

# Logger
LOGGER_NAME = 'App.Processes.SaveVideo'
LOG = logging.getLogger(LOGGER_NAME)


class SaveVideoLogger(QObject, TqdmProgressBarLogger):
    """
    The class for get the status of the MoviePy process.

    ...

    Attributes
    ----------
    logger_audio : signal
        the signal to change the save audio progress bar
    logger_video : signal
        the signal to change the save video progress bar
    audio_or_video : str
        the process in working ('audio' or 'video')

    """

    # Signals
    logger_audio = QtCore.pyqtSignal(int)
    logger_video = QtCore.pyqtSignal(int)

    # Process working
    audio_or_video = None

    def callback(self, **changes):
        for (_, new_value) in changes.items():
            if 'Writing audio' in new_value:
                self.audio_or_video = 'audio'
            elif 'Writing video' in new_value:
                self.audio_or_video = 'video'
            else:
                self.audio_or_video = None

    def bars_callback(self, bar, attr, value, old_value):
        super().bars_callback(bar, attr, value, old_value)

        if self.audio_or_video is not None and attr == 'index':
            actual_bar = self.tqdm_bars[bar]
            if actual_bar is not None:
                if self.audio_or_video == 'audio':
                    self.logger_audio.emit(actual_bar.n / actual_bar.total * 100)
                elif self.audio_or_video == 'video':
                    self.logger_video.emit(actual_bar.n / actual_bar.total * 100)
        # TODO: Remove progress bar at the console


class SaveVideo(QThread):
    """
    The save video process.

    ...

    Attributes
    ----------
    progress_cut : signal
        the signal to change the cut video progress bar
    progress_audio : signal
        the signal to change the save audio progress bar
    progress_video : signal
        the signal to change the save video progress bar
    logger : SaveVideoLogger
        the SaveVideoLogger to get the save audio and video progress bar
    scenes_process : process
        the process of the scene analysis
    objects_process : process
        the process of the objects analysis
    subtitles_process : process
        the process of the subtitle analysis
    resume_process : process
        the process of the resume

    Methods
    -------
    restart_process()
        restart the save video process
    activate_process()
        activate the save video process
    deactivate_process()
        deactivate the save video process

    """

    # Signals
    progress_cut = QtCore.pyqtSignal(int)
    progress_audio = QtCore.pyqtSignal(int)
    progress_video = QtCore.pyqtSignal(int)

    # Logger
    logger = SaveVideoLogger()

    # Processes to wait
    scenes_process = None
    objects_process = None
    subtitles_process = None
    resume_process = None

    def __init__(self, scenes_process, objects_process, subtitles_process, resume_process):
        LOG.debug('initializing save video process')
        QThread.__init__(self)
        self.active = True
        self.restart = False
        self.scenes_process = scenes_process
        self.objects_process = objects_process
        self.subtitles_process = subtitles_process
        self.resume_process = resume_process

        self.logger.logger_audio.connect(self.progress_audio)
        self.logger.logger_video.connect(self.progress_video)

        LOG.info('save video process initialized')

    def run(self):
        """
        Method that save the final video.
        """
        while True:
            LOG.debug('starting save video')
            self.active = True
            self.restart = False

            # Wait to the previous processes' finish
            if self.active:
                LOG.debug('waiting previous processes')
                self.scenes_process.wait()
                self.objects_process.wait()
                self.subtitles_process.wait()
                self.resume_process.wait()

            # Load the original video to "clip"
            if self.active:
                LOG.debug('loading the original video')
                with GeneralContext(read_only=True) as manager:
                    path = manager.final_video_path
                    resume_times = manager.resume_times
                    clip = load_video(manager.original_video_path)
                LOG.debug('original video loaded')

            # Get and concatenate the sub clips for the final video
            if self.active:
                LOG.debug('getting and concatenating the sub clips')
                clips = []
                for index, sub_times in enumerate(resume_times):
                    clips.append(clip.subclip(sub_times[0] / 1000, sub_times[1] / 1000))
                    self.progress_cut.emit(index / len(resume_times) * 100)
                final_clip = concatenate_videoclips(clips)
                self.progress_cut.emit(100)
                LOG.debug('sub clips gotten and concatenated')

            # Save the video into the final video's path
            if self.active:
                LOG.debug('saving final video')
                final_clip.write_videofile(path, logger=self.logger, verbose=False)
                self.progress_audio.emit(100)
                self.progress_video.emit(100)
                LOG.info('final video saved')

            LOG.debug('ending video save')

            if not self.restart:
                break

    def restart_process(self):
        """ Method that restart the save video process."""
        self.deactivate_process()
        self.restart = True
        self.progress_cut.emit(0)
        self.progress_audio.emit(0)
        self.progress_video.emit(0)
        LOG.info('save video process restart activate')

    def activate_process(self):
        """ Method that activate the save video process."""
        self.active = True
        LOG.info('save video process activate')

    def deactivate_process(self):
        """ Method that deactivate the save video process."""
        self.active = False
        LOG.info('save video process deactivate')
