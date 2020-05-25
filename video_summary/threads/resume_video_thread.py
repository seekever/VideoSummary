""" The module for the resume's thread."""

import logging

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from video_summary.context.general_context import GeneralContext, ResumeMode
from video_summary.context.objects_context import ObjectsContext
from video_summary.context.scenes_context import ScenesContext
from video_summary.context.subtitles_context import SubtitlesContext
from video_summary.utils import normalize_times

# Logger
LOGGER_NAME = 'App.Threads.Resume'
LOG = logging.getLogger(LOGGER_NAME)


class Resume(QThread):
    """
    The resume thread.

    ...

    Attributes
    ----------
    progress : signal
        the signal to change the progress bar
    scenes_thread : thread
        the thread of the scene analysis process
    objects_thread : thread
        the thread of the objects analysis process
    subtitles_thread : thread
        the thread of the subtitle analysis process

    Methods
    -------
    restart_thread()
        restart the resume's thread
    activate_thread()
        activate the resume's thread
    deactivate_thread()
        deactivate the resume's thread

    """

    # Signals
    progress = QtCore.pyqtSignal(int)

    # Threads to wait
    scenes_thread = None
    objects_thread = None
    subtitles_thread = None

    def __init__(self, scenes_thread, objects_thread, subtitles_thread):
        LOG.debug('initializing resume\'s thread')
        QThread.__init__(self)
        self.active = True
        self.restart = False
        self.scenes_thread = scenes_thread
        self.objects_thread = objects_thread
        self.subtitles_thread = subtitles_thread
        LOG.info('resume\'s thread initialized')

    def run(self):
        """ Method that resume the original video."""
        while True:
            LOG.debug('starting resume')
            self.active = True
            self.restart = False

            # Wait to the previous threads' finish
            if self.active:
                LOG.debug('waiting previous process')
                self.scenes_thread.wait()
                self.objects_thread.wait()
                self.subtitles_thread.wait()

            # Load general configurations
            if self.active:
                result = []
                with GeneralContext(read_only=True) as manager:
                    mode = manager.resume_mode
                    detect_scenes = manager.detect_scenes
                self.progress.emit(20)

            # Add the times of the subtitles
            if self.active:
                if mode in (ResumeMode.SUBTITLES, ResumeMode.SUBTITLES_AND_OBJECTS):
                    LOG.debug('adding subtitles times')
                    with SubtitlesContext(read_only=True) as manager:
                        result = sorted(manager.subtitles_list, key=lambda x: x.score, reverse=True)
                        result = result[: int(len(result) * manager.resume_percentage / 100)]
                        result = [x.get_times() for x in result]
                    LOG.debug('subtitles times added')
                self.progress.emit(40)

            # Add the times of the objects
            if self.active:
                if mode in (ResumeMode.OBJECTS, ResumeMode.SUBTITLES_AND_OBJECTS):
                    LOG.debug('adding objects times')
                    with ObjectsContext(read_only=True) as manager:
                        for key in list(
                                set(manager.objects_list).intersection(
                                    manager.objects_dict.keys())):
                            object_times = manager.objects_dict.get(key)
                            for object_time in object_times:
                                result.append([object_time - 10, object_time + 10])
                    LOG.debug('objects times added')
                self.progress.emit(60)

            # Adjust the times to the scenes
            if self.active:
                if detect_scenes:
                    LOG.debug('adjusting times to scenes')
                    with ScenesContext(read_only=True) as manager:
                        for index, time in enumerate(result):
                            scene_ini = [s for s in manager.scenes_list if time[0] <= s[1]][0]
                            result[index][0] = scene_ini[0]
                            scene_fin = [s for s in manager.scenes_list if time[1] <= s[1]][0]
                            result[index][1] = scene_fin[1]
                    LOG.debug('times adjusted to scenes')
                self.progress.emit(80)

            # Normalize and save resume times
            if self.active:
                LOG.debug('normalizing times')
                result = sorted(result, key=lambda times: times[0])
                result = normalize_times(result)
                with GeneralContext() as manager:
                    manager.resume_times = []
                    for x in result:
                        manager.resume_times.append(x)
                LOG.debug('times normalized')

            if self.active:
                self.progress.emit(100)

            LOG.debug('ending resume')

            if not self.restart:
                break

    def restart_thread(self):
        """ Method that restart the resume\'s thread."""
        self.deactivate_thread()
        self.restart = True
        self.progress.emit(0)
        LOG.info('resume\'s thread restart activate')

    def activate_thread(self):
        """ Method that activate the resume\'s thread."""
        self.active = True
        LOG.info('resume\'s thread activate')

    def deactivate_thread(self):
        """ Method that deactivate the resume\'s thread."""
        self.active = False
        LOG.info('resume\'s thread deactivate')
