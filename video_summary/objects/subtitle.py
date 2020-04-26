"""The module which represents a Subtitle object."""

# Strings for JSON
SUBTITLE_TEXT = "text"
SUBTITLE_START = "start"
SUBTITLE_END = "end"
SUBTITLE_SCORE = "score"


class Subtitle:
    """
    A class used to represent the subtitles.

    ...

    Attributes
    ----------
    text : str
        the subtitle text
    start : int
        the start time in milliseconds
    end : int
        the end time in milliseconds
    score: int
        the subtitle importance score

    Methods
    -------
    set_times(start, end)
        set start and end times to a Subtitle
    get_times()
        get start and end times like a list [start, end]
    """

    def __init__(self, text, start, end, score):
        self.text = text
        self.start = start
        self.end = end
        self.score = score

    def set_times(self, start, end):
        """
        The method to set start and end times to a Subtitle.

        Parameters
        ----------
        start : int
            the start time in milliseconds
        end : int
            the end time in milliseconds
        """

        self.start = start
        self.end = end

    def get_times(self):
        """
        The method to get start and end times like a list [start, end].

        Returns
        -------
        list
            a list with the start and the end in milliseconds
        """

        return [self.start, self.end]


def to_dict(subtitle):
    """
    The method to parse a Subtitle to a dictionary.

    Parameters
    ----------
    subtitle : Subtitle
        the Subtitle to parse

    Returns
    -------
    dict
        a dict with the Subtitle data
    """

    if subtitle is None:
        return None

    result = dict()
    result[SUBTITLE_TEXT] = subtitle.text
    result[SUBTITLE_START] = subtitle.start
    result[SUBTITLE_END] = subtitle.end
    result[SUBTITLE_SCORE] = subtitle.score
    return result


def to_dict_list(subtitle_list):
    """
    The method to parse a list of Subtitles to a list of dictionaries.

    Parameters
    ----------
    subtitle_list : list
        the list of Subtitles to parse

    Returns
    -------
    list
        a list of dicts with the Subtitles data
    """
    if subtitle_list is None:
        return None

    result = list()
    for subtitle in subtitle_list:
        result.append(to_dict(subtitle))
    return result


def from_dict(dictionary):
    """
    The method to parse a dictionary to a Subtitle.

    Parameters
    ----------
    dictionary : dict
        the dictionary to parse

    Returns
    -------
    Subtitle
        a Subtitle with the dictionary data
    """
    if dictionary is None:
        return None

    result = Subtitle(None, None, None, None)
    result.text = dictionary[SUBTITLE_TEXT]
    result.start = dictionary[SUBTITLE_START]
    result.end = dictionary[SUBTITLE_END]
    result.score = dictionary[SUBTITLE_SCORE]
    return result


def from_dict_list(dictionary_list):
    """
    The method to parse a list of dictionaries to a list of Subtitles.

    Parameters
    ----------
    dictionary_list : list
        the list of dictionaries to parse

    Returns
    -------
    list
        a list of Subtitles with the dictionaries data
    """
    if dictionary_list is None:
        return None

    result = list()
    for dictionary in dictionary_list:
        result.append((from_dict(dictionary)))
    return result
