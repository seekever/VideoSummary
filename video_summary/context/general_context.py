"""The context which manages the general configurations."""

import json
import os

from enum import Enum

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'GeneralConfig.conf')

# Strings for JSON
RESUME_MODE = "resumeMode"
DETECT_SCENES = "detectScenes"


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
    resume_mode : str
        the resume mode (Subtitles, Objects or Subtitles and objects)
    detect_scenes : bool
        a boolean to activate the scene detection

    """

    def __init__(self):
        self.config = None
        self.resume_mode = None
        self.detect_scenes = None

    def __enter__(self):
        try:
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
        except FileNotFoundError:
            self.config = {}

        self.resume_mode = self.config.get(RESUME_MODE)
        self.detect_scenes = self.config.get(DETECT_SCENES)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.config[RESUME_MODE] = self.resume_mode
        self.config[DETECT_SCENES] = self.detect_scenes

        json_string = json.dumps(self.config)

        with open(CONFIG_PATH, 'w') as json_file:
            json_file.write(json_string)

        json_file.close()
