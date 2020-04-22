"""The context which manages the subtitles configurations."""
import json
import os
from enum import Enum

from video_summary.objects.subtitle import from_dict_list, to_dict_list

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'SubtitlesConfig.conf')

# Strings for JSON
SUBTITLES_LIST = "subtitlesList"
RESUME_PERCENTAGE = "resumePercentage"
VECTORING_TYPE = "vectoringType"
REMOVE_PUNCTUATION = "removePunctuation"
PUNCTUATION_SIGNS = "punctuationSigns"
REMOVE_STOP_WORDS = "removeStopWords"
REMOVE_CAPITAL_LETTERS = "removeCapitalLetters"
REMOVE_ACCENTS = "removeAccents"
LANGUAGE = "language"


# Parametrization
class VectoringType(int, Enum):
    """ Parametrization for the vectoring type."""
    COUNTERS = 1
    BINARIES_COUNTERS = 2
    N_GRAM_COUNTERS = 3
    TF_WITH_NORMALIZATION_L1 = 4
    TF_WITH_NORMALIZATION_L2 = 5
    TF_IDF = 6
    TF_IDF_WITH_SMOOTHING_IDF = 7
    TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L1 = 8
    TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L2 = 9


class Languages(str, Enum):
    """ Parametrization for the vectoring type."""
    ARABIC = "arabic"
    AZERBAIJANI = "azerbaijani"
    DANISH = "danish"
    DUTCH = "dutch"
    ENGLISH = "english"
    FINNISH = "finnish"
    FRENCH = "french"
    GERMAN = "german"
    GREEK = "greek"
    HUNGARIAN = "hungarian"
    INDONESIAN = "indonesian"
    ITALIAN = "italian"
    KAZAKH = "kazakh"
    NEPALI = "nepali"
    NORWEGIAN = "norwegian"
    PORTUGUESE = "portuguese"
    ROMANIAN = "romanian"
    RUSSIAN = "russian"
    SPANISH = "spanish"
    SWEDISH = "swedish"
    TURKISH = "turkish"


class SubtitlesContext:
    """
    A class used to represent the video subtitles context.

    ...

    Attributes
    ----------
    config : dict
        a dict with all the general settings
    subtitles_list : list
        a list of Subtitles objects
    resume_percentage : float
        the resume percentage of the subtitles (0.0 - 1.0)
    vectoring_type : int
        the vectoring type (class VectoringType)
    remove_punctuation : bool
        a boolean to activate the punctuation remove
    punctuation_signs : list
        a char list with all the punctuation signs to remove
    remove_stop_words : bool
        a boolean to activate the stop words remove
    remove_capital_letters : bool
        a boolean to activate the capital letters remove
    remove_accents : bool
        a boolean to activate the accents remove
    language : string
         the subtitles language (class Language)

    """

    def __init__(self):
        self.config = None
        self.subtitles_list = None
        self.resume_percentage = None
        self.vectoring_type = None
        self.remove_punctuation = None
        self.punctuation_signs = None
        self.remove_stop_words = None
        self.remove_capital_letters = None
        self.remove_accents = None
        self.language = None

    def __enter__(self):
        try:
            with open(CONFIG_PATH, 'r') as json_file:
                json_string = json_file.read()
                self.config = json.loads(json_string)
        except FileNotFoundError:
            self.config = {}

        self.subtitles_list = from_dict_list(self.config.get(SUBTITLES_LIST))
        self.resume_percentage = self.config.get(RESUME_PERCENTAGE)
        self.vectoring_type = self.config.get(VECTORING_TYPE)
        self.remove_punctuation = self.config.get(REMOVE_PUNCTUATION)
        self.punctuation_signs = self.config.get(PUNCTUATION_SIGNS)
        self.remove_stop_words = self.config.get(REMOVE_STOP_WORDS)
        self.remove_capital_letters = self.config.get(REMOVE_CAPITAL_LETTERS)
        self.remove_accents = self.config.get(REMOVE_ACCENTS)
        self.language = self.config.get(LANGUAGE)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.config[SUBTITLES_LIST] = to_dict_list(self.subtitles_list)
        self.config[RESUME_PERCENTAGE] = self.resume_percentage
        self.config[VECTORING_TYPE] = self.vectoring_type
        self.config[REMOVE_PUNCTUATION] = self.remove_punctuation
        self.config[PUNCTUATION_SIGNS] = self.punctuation_signs
        self.config[REMOVE_STOP_WORDS] = self.remove_stop_words
        self.config[REMOVE_CAPITAL_LETTERS] = self.remove_capital_letters
        self.config[REMOVE_ACCENTS] = self.remove_accents
        self.config[LANGUAGE] = self.language

        json_string = json.dumps(self.config, indent=4)

        with open(CONFIG_PATH, 'w') as json_file:
            json_file.write(json_string)

        json_file.close()
