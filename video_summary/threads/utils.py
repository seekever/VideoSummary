"""Module with the utils for the threads"""

from moviepy.editor import VideoFileClip


def load_video(video_path):
    """
    Method that load the video and return the clip.

    ...

    Attributes
    ----------
    video_path : str
        the video path

    Returns
    -------
    clip
        the video clip
    """

    return VideoFileClip(video_path)


def get_sec(time_str):
    """
    Method to get seconds from string time.

    ...

    Attributes
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


def get_time_from_line(string):
    """
    Method to get the time from a ffmpeg output string.

    ...

    Attributes
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
        return string[time_ind + len(time_ind):bitrate_ind]
    return None
