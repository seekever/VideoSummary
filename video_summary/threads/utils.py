"""Module with the utils for the threads"""
import cv2
import numpy as np
from moviepy.editor import VideoFileClip


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


def get_sec(time_str):
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
