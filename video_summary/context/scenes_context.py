"""The context which manages the scenes configurations"""

import json
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'ScenesConfig.conf')

# Strings for JSON
SCENES_LIST = "scenesList"


class ScenesContext:
    """
    A class used to represent the video scene context

    ...

    Attributes
    ----------
    config : dict
        a dict with all the general settings
    scenes_list : list [int, int]
        a list with int tuples (initialTime, endTime)

    """

    def __init__(self):
        self.config = None
        self.scenes_list = None

    def __enter__(self):
        try:
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
        except FileNotFoundError:
            self.config = {}

        self.scenes_list = self.config.get(SCENES_LIST)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.config[SCENES_LIST] = self.scenes_list

        json_string = json.dumps(self.config)

        with open(CONFIG_PATH, 'w') as json_file:
            json_file.write(json_string)
        json_file.close()
