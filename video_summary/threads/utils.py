"""Module with the utils for the threads"""

from copy import copy

import cv2
import numpy as np
import pysrt
import unidecode
from moviepy.editor import VideoFileClip
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from video_summary.context.subtitles_context import VectoringType
from video_summary.objects.subtitle import Subtitle

# Switcher
VECTORING_SWITCHER = {
    VectoringType.COUNTERS: CountVectorizer(),
    VectoringType.BINARIES_COUNTERS: CountVectorizer(binary=True),
    VectoringType.N_GRAM_COUNTERS: CountVectorizer(ngram_range=(1, 4)),
    VectoringType.TF_WITH_NORMALIZATION_L1: TfidfVectorizer(norm='l1', use_idf=False),
    VectoringType.TF_WITH_NORMALIZATION_L2: TfidfVectorizer(norm='l2', use_idf=False),
    VectoringType.TF_IDF: TfidfVectorizer(norm=None, smooth_idf=False),
    VectoringType.TF_IDF_WITH_SMOOTHING_IDF: TfidfVectorizer(norm=None, smooth_idf=True),
    VectoringType.TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L1:
        TfidfVectorizer(norm='l1', smooth_idf=True),
    VectoringType.TF_IDF_WITH_SMOOTHING_IDF_AND_NORMALIZATION_L2: TfidfVectorizer()
}


def load_video(video_path):
    """
    Method that load the video and return the clip.

    ...

    Parameters
    ----------
    video_path : str
        the video path

    Returns
    -------
    clip
        the video clip
    """

    return VideoFileClip(video_path)


def get_sec_from_string(time_str):
    """
    Method to get seconds from string time.

    ...

    Parameters
    ----------
    time_str : str
        the string time with format HH:mm:ss

    Returns
    -------
    float
        the time_str in seconds
    """

    hours, minutes, seconds = time_str.split(':')
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def get_milli_sec_from_sub(time_sub):
    """
    Method to get seconds from SubRipTime.

    ...

    Parameters
    ----------
    time_sub : SubRipTime
        the SubRipTime object with the time

    Returns
    -------
    float
        the time_sub in seconds
    """

    return float((time_sub.hours * 3600 + time_sub.minutes * 60 + time_sub.seconds)
                 * 1000 + time_sub.milliseconds)


def get_time_from_line(string):
    """
    Method to get the time from a ffmpeg output string.

    ...

    Parameters
    ----------
    string : str
        the string time with format HH:mm:ss

    Returns
    -------
    str
        a string with the time with format HH:mm:ss or None
    """

    time_ind = string.find("time=")
    bitrate_ind = string.find("bitrate=")
    if time_ind >= 0:
        return string[time_ind + 5:bitrate_ind]
    return None


def load_yolo(weights_path, cfg_path, names_path):
    """
    Method to load the Yolo's net.

    ...

    Parameters
    ----------
    weights_path : str
        the Yolo's weights path
    cfg_path : str
        the Yolo's cfg path
    names_path : str
        the Yolo's names path

    Returns
    -------
    net
        the Yolo's net
    list
        a list of strings with the classes names
    list
        a list of strings with the layers names

    """

    net = cv2.dnn.readNet(weights_path, cfg_path)
    with open(names_path, "r") as file:
        classes = [line.strip() for line in file.readlines()]
    layers_names = net.getLayerNames()
    output_layers = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers


def detect_objects(frame, net, output_layers, classes):
    """
    Method to detect the objects in a frame.

    ...

    Parameters
    ----------
    frame : array
        a numpy array representing the RGB picture of the clip
    net : net
        the Yolo's net
    output_layers : list
        a list of strings with the layers names
    classes : list
        a list of strings with the classes names

    Returns
    -------
    list
        a list of strings with the detected objects names

    """

    frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
    blob = cv2.dnn.blobFromImage(frame, scalefactor=0.00392, size=(320, 320),
                                 mean=(0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    result = []
    for output in outputs:
        for detect in output:
            scores = detect[5:]
            class_id = np.argmax(scores)
            result.append(classes[class_id])
    return set(result)


def fuse_subtitles(first_sub, second_sub):
    """
    Method to fuse two subtitles.

    ...

    Parameters
    ----------
    first_sub : Subtitle
        the first subtitle
    second_sub : Subtitle
        the second subtitle

    Returns
    -------
    Subtitle
        a new subtitle with the fuse's result

    """

    if first_sub is None:
        return second_sub
    if second_sub is None:
        return first_sub

    result = copy(first_sub)

    if result.text is None:
        result.text = second_sub.text
    elif second_sub.text is not None:
        result.text += " " + second_sub.text

    if result.start is None:
        result.start = second_sub.start
    elif second_sub.start is not None:
        result.start = min(result.start, second_sub.start)

    if result.end is None:
        result.end = second_sub.end
    elif second_sub.end is not None:
        result.end = max(result.end, second_sub.end)

    if result.score is None:
        result.score = second_sub.score
    elif second_sub.score is not None:
        result.score += second_sub.score

    return result


def join_phrases(subtitles_list):
    """
    Method to join the text of the successive subtitles.

    ...

    Parameters
    ----------
    subtitles_list : list
        a subtitles list

    Returns
    -------
    list
        a new subtitles list with the successive subtitles joined

    """

    if subtitles_list is None:
        return None

    actual_sub = None
    result = []
    for sub in subtitles_list:
        if sub is not None:
            if actual_sub is None:
                actual_sub = sub
            else:
                actual_sub = fuse_subtitles(actual_sub, sub)

            if actual_sub.text is not None and actual_sub.text[-1] in '¡!.¿?':
                result.append(actual_sub)
                actual_sub = None
    return result


def clean_phrases(subtitles_list, remove_capital_letters=False, remove_stop_words=False,
                  remove_punctuation=False, remove_accents=False, remove_all=False, stop_words=None,
                  punctuation_signs=None):
    """
    Method to clean the text of the subtitles.

    ...

    Parameters
    ----------
    subtitles_list : list
        a subtitles list
    remove_capital_letters : bool
        a boolean to activate the removal of capital letters
    remove_stop_words : bool
        a boolean to activate the removal of stop words
    remove_punctuation : bool
        a boolean to activate the removal of punctuations
    remove_accents : bool
        a boolean to activate the removal of accents
    remove_all : bool
        a boolean to activate all previous removals
    stop_words : list
        a list of strings with all the stop words to remove
    punctuation_signs : list
        a list of chars with all the punctuation signs to remove

    Returns
    -------
    list
        a new subtitles list with the text of the subtitles cleaned

    """

    if subtitles_list is None:
        return None

    result = []
    if punctuation_signs is None:
        punctuation_signs = []
    punctuation_table = str.maketrans(
        {key: None for key in punctuation_signs})

    for sub in subtitles_list:
        if sub is not None:
            if sub.text is not None:
                if remove_capital_letters or remove_all:
                    sub.text = sub.text.lower()
                if remove_stop_words or remove_all:
                    sub.text = ' '.join([word for word in sub.text.split()
                                         if word.lower() not in stop_words])
                if remove_punctuation or remove_all:
                    sub.text = sub.text.translate(punctuation_table)
                if remove_accents or remove_all:
                    sub.text = unidecode.unidecode(sub.text)
            result.append(sub)
    return result


def load_subtitles(path):
    """
    Method to load the subtitles.

    ...

    Parameters
    ----------
    path : str
        the subtitles' path

    Returns
    -------
    list
        a list of subtitles

    """

    subtitles = pysrt.open(path)
    subtitles_list = []
    for sub in subtitles:
        sub_start = get_milli_sec_from_sub(sub.start)
        sub_end = get_milli_sec_from_sub(sub.end)
        subtitles_list.append(Subtitle(sub.text, sub_start, sub_end, -1))
    return subtitles_list


def normalize_times(times):
    """
    Method to normalize a list of times.

    ...

    Parameters
    ----------
    times : list
        the times' list with int pairs (start, end)

    Returns
    -------
    list
        the times' list with int pairs (start, end) normalized

    """

    if times is None:
        return None

    result = []
    last = -99
    for time in times:
        if time is not None:
            if last + 1 < time[0]:
                result.append(time)
            else:
                last = max(last, time[1])
                result[-1][1] = last
            last = result[-1][1]

    return result
