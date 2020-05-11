"""The context which manages the general configurations."""

import json
import logging
import os

from enum import Enum

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'GeneralConfig.conf')

# Strings for JSON
ORIGINAL_VIDEO_PATH = "originalVideoPath"
RESUME_MODE = "resumeMode"
DETECT_SCENES = "detectScenes"
SCENES_DIFFERENCE = "scenesDifference"
RESUME_TIMES = "resumeTimes"

# Logger
LOGGER_NAME = 'App.Context.General'
LOG = logging.getLogger(LOGGER_NAME)


# Parametrization
class ResumeMode(int, Enum):
    """ Parametrization for the resume mode."""
    SUBTITLES = 0
    OBJECTS = 1
    SUBTITLES_AND_OBJECTS = 2


class GeneralContext:
    """
    A class used to represent the application general context.

    ...

    Attributes
    ----------
    read_only : bool
        a boolean to activate the read only mode
    config : dict
        a dict with all the general settings
    original_video_path : str
        the original video's path
    resume_mode : int
        the resume mode (class ResumeMode)
    detect_scenes : bool
        a boolean to activate the scene detection
    scenes_difference : float
        the difference percentage between scenes
    resume_times : list
        a list of pair of ints (start, end)

    """

    def __init__(self, read_only=False):
        LOG.debug('starting general context')
        self.read_only = read_only
        self.config = None
        self.original_video_path = None
        self.resume_mode = None
        self.detect_scenes = None
        self.scenes_difference = None
        self.resume_times = None
        LOG.debug('general context started')

    def __enter__(self):
        try:
            LOG.debug('reading general context')
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
                LOG.info('general context read from %s', CONFIG_PATH)
        except FileNotFoundError:
            LOG.debug('general context not found')
            LOG.debug('creating general context')
            self.config = {}
            LOG.debug('general context created')

        LOG.debug('loading general context')
        self.original_video_path = self.config.get(ORIGINAL_VIDEO_PATH)
        self.resume_mode = self.config.get(RESUME_MODE)
        self.detect_scenes = self.config.get(DETECT_SCENES)
        self.scenes_difference = self.config.get(SCENES_DIFFERENCE)
        self.resume_times = self.config.get(RESUME_TIMES)
        LOG.debug('general context loaded')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.read_only:
            LOG.debug('saving general context')
            self.config[ORIGINAL_VIDEO_PATH] = self.original_video_path
            self.config[RESUME_MODE] = self.resume_mode
            self.config[DETECT_SCENES] = self.detect_scenes
            self.config[SCENES_DIFFERENCE] = self.scenes_difference
            self.config[RESUME_TIMES] = self.resume_times
            LOG.debug('general context saved')

            LOG.debug('writing general context')
            json_string = json.dumps(self.config, indent=4)

            with open(CONFIG_PATH, 'w') as json_file:
                json_file.write(json_string)

            json_file.close()
            LOG.info('general context written at %s', CONFIG_PATH)
