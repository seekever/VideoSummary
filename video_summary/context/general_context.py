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

# Logger
LOGGER_NAME = 'App.Context.General'
LOG = logging.getLogger(LOGGER_NAME)


# Parametrization
class ResumeMode(int, Enum):
    """ Parametrization for the resume mode."""
    SUBTITLES = 1
    OBJECTS = 2
    SUBTITLES_AND_OBJECTS = 3


class GeneralContext:
    """
    A class used to represent the application general context.

    ...

    Attributes
    ----------
    config : dict
        a dict with all the general settings
    original_video_path : str
        the original video's path
    resume_mode : int
        the resume mode (class ResumeMode)
    detect_scenes : bool
        a boolean to activate the scene detection

    """

    def __init__(self):
        LOG.debug('starting general context')
        self.config = None
        self.original_video_path = None
        self.resume_mode = None
        self.detect_scenes = None
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
        LOG.debug('general context loaded')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOG.debug('saving general context')
        self.config[ORIGINAL_VIDEO_PATH] = self.original_video_path
        self.config[RESUME_MODE] = self.resume_mode
        self.config[DETECT_SCENES] = self.detect_scenes
        LOG.debug('general context saved')

        LOG.debug('writing general context')
        json_string = json.dumps(self.config, indent=4)

        with open(CONFIG_PATH, 'w') as json_file:
            json_file.write(json_string)

        json_file.close()
        LOG.info('general context written at %s', CONFIG_PATH)
