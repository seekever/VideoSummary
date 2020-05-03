""" The module for the scenes analysis thread."""

import logging
import os
import subprocess

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from video_summary.context.general_context import GeneralContext
from video_summary.context.scenes_context import ScenesContext
from video_summary.threads.utils import load_video, get_time_from_line, get_sec

# Logger
LOGGER_NAME = 'App.Threads.SceneAnalysis'
LOG = logging.getLogger(LOGGER_NAME)


class ScenesAnalysis(QThread):
    """
    The scenes analysis thread.

    ...

    Attributes
    ----------
    progress : signal
        the signal to change the progress bar

    Methods
    -------
    restart_thread()
        restart the scenes analysis thread
    activate_thread()
        activate the scenes analysis thread
    deactivate_thread()
        deactivate the scenes analysis thread

    """

    # Signals
    progress = QtCore.pyqtSignal(int)

    def __init__(self):
        LOG.debug('initializing scene analysis thread')
        QThread.__init__(self)
        self.active = True
        self.restart = False
        LOG.info('scenes analysis thread initialized')

    def run(self):
        """ Method that analysis the scenes and save the scenes list in the ScenesContext."""
        while True:
            LOG.debug('starting scenes analysis')
            self.active = True
            self.restart = False

            # Load the original video to "clip"
            if self.active:
                LOG.debug('loading the original video')
                with GeneralContext(read_only=True) as manager:
                    path = manager.original_video_path
                    diff = manager.scenes_difference
                clip = load_video(path)
                LOG.debug('original video loaded')

            # Detect the different scenes and save them at the "timestamps" file
            if self.active:
                LOG.debug('detecting scenes')
                cmd = ['ffmpeg', '-progress', 'progress.txt', '-i', path, '-filter:v',
                       "select='gt(scene," + str(diff) + ")',showinfo", '-f', 'null', '-']

                LOG.debug('starting subprocess')
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

                with open('ffout', 'w') as file:
                    for line in proc.stdout:
                        string = line.decode("utf-8")
                        time_str = get_time_from_line(string)
                        if time_str is not None:
                            actual_time = get_sec(time_str)
                            if self.active:
                                self.progress.emit(int(actual_time / clip.duration * 100))
                        file.writelines(string)

                os.system('grep showinfo ffout | grep pts_time:[0-9.]* -o | '
                          'grep [0-9.]* -o > timestamps')
                LOG.debug('scenes detected')

            # Read scenes to the "timestamps" file and save them to the ScenesContext
            if self.active:
                LOG.debug('saving scenes list')
                with ScenesContext() as manager:
                    manager.scenes_list = []
                    with open('timestamps') as file:
                        before = 0
                        for line in file:
                            now = int(float(line[:-1]) * 1000)
                            manager.scenes_list.append([before, now])
                            before = now + 1
                    manager.scenes_list.append([before, int(clip.duration * 1000)])
                LOG.debug('scenes list saved')

            if self.active:
                self.progress.emit(100)

            # Delete temporal files
            os.system('rm ffout')
            os.system('rm timestamps')
            os.system('rm progress.txt')
            LOG.debug('ending scenes analysis')

            if not self.restart:
                break

    def restart_thread(self):
        """ Method that restart the scenes analysis thread."""
        self.deactivate_thread()
        self.restart = True
        self.progress.emit(0)
        LOG.info('scenes analysis thread restart activate')

    def activate_thread(self):
        """ Method that activate the scenes analysis thread."""
        self.active = True
        LOG.info('scenes analysis thread activate')

    def deactivate_thread(self):
        """ Method that deactivate the scenes analysis thread."""
        self.active = False
        LOG.info('scenes analysis thread deactivate')
