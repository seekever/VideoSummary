"""The module for the objects analysis process."""

import logging
import os
from collections import defaultdict

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from video_summary.context.general_context import GeneralContext
from video_summary.context.objects_context import ObjectsContext
from video_summary.context.scenes_context import ScenesContext
from video_summary.utils import load_video, load_yolo, detect_objects

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Logger
LOGGER_NAME = 'App.Processes.ObjectsAnalysis'
LOG = logging.getLogger(LOGGER_NAME)


class ObjectsAnalysis(QThread):
    """
    The objects analysis process.

    ...

    Attributes
    ----------
    progress : signal
        the signal to change the progress bar
    scenes_process : process
        the process of the scene analysis

    Methods
    -------
    restart_process()
        restart the objects analysis process
    activate_process()
        activate the objects analysis proces
    deactivate_process()
        deactivate the objects analysis process

    """

    # Signals
    progress = QtCore.pyqtSignal(int)

    # Processes to wait
    scenes_process = None

    def __init__(self, scenes_process):
        LOG.debug('initializing objects analysis process')
        QThread.__init__(self)
        self.active = True
        self.restart = False
        self.scenes_process = scenes_process
        LOG.info('objects analysis process initialized')

    def run(self):
        """ Method that analysis the objects and save the objects dict in the ObjectsContext."""
        while True:
            LOG.debug('starting objects analysis')
            self.active = True
            self.restart = False

            # Load the original video to "clip"
            if self.active:
                LOG.debug('loading the original video')
                with GeneralContext(read_only=True) as manager:
                    path = manager.original_video_path
                clip = load_video(path)
                LOG.debug('original video loaded')

            # Wait to the previous process' finish
            if self.active:
                LOG.debug('waiting previous process')
                self.scenes_process.wait()

            # Load scenes list
            if self.active:
                with ScenesContext(read_only=True) as manager:
                    LOG.debug('loading the scenes list')
                    scenes_list = manager.scenes_list
                    LOG.debug('scenes list loaded')

            with ObjectsContext(read_only=True) as manager:
                # Load yolo
                if self.active:
                    LOG.debug('loading Yolo\'s darknet')
                    model, classes, output_layers = load_yolo(
                        manager.yolo_weights_path, manager.yolo_cfg_path, manager.yolo_names_path)
                    LOG.debug('Yolo\'s darknet loaded')

                # Get scenes to analyse
                if self.active:
                    if manager.optimization:
                        LOG.debug('objects analysis optimization active')
                        milli_sec_to_analyse = []
                        for scene in scenes_list:
                            for i in range(1, manager.scenes_periodicity + 1):
                                milli_sec_to_analyse.append(
                                    scene[0] + ((scene[1] - scene[0]) *
                                                (i / (manager.scenes_periodicity + 1))))
                    else:
                        LOG.debug('objects analysis optimization not active')
                        milli_sec_to_analyse = list(
                            range(1, int(clip.duration) * 1000, manager.milliseconds_periodicity))

            # Detect objects and save them in ObjectsContext
            if self.active:
                LOG.debug('starting objects detection')
                with ObjectsContext() as manager:
                    manager.objects_dict = defaultdict(list)
                    for index, milli_sec in enumerate(milli_sec_to_analyse):
                        if self.active:
                            frame = clip.get_frame(milli_sec / 1000)
                            objects = detect_objects(frame, model, output_layers, classes)
                            for obj in objects:
                                manager.objects_dict[obj].append(milli_sec)
                            self.progress.emit(index / len(milli_sec_to_analyse) * 100)
                        else:
                            break
                LOG.debug('objects detection ended')

            if self.active:
                self.progress.emit(100)

            LOG.debug('ending objects analysis')

            if not self.restart:
                break

    def restart_process(self):
        """ Method that restart the objects analysis process."""
        self.active = False
        self.restart = True
        self.progress.emit(0)
        LOG.info('objects analysis process restart activate')

    def activate_process(self):
        """ Method that activate the objects analysis process."""
        self.active = True
        LOG.info('objects analysis process activate')

    def deactivate_process(self):
        """ Method that deactivate the objects analysis process."""
        self.active = False
        LOG.info('objects analysis process deactivate')
