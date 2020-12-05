from os import listdir
from os.path import isfile, join, splitext, split

from enum import Enum

from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QValidator, QRegularExpressionValidator

IMAGE_FORMATS = ["bmp", "gif", "jpg", "jpeg", "png", "pbm", "pgm", "ppm", "xbm", "xpm"]
VIDEO_FORMATS = ["avi", "mkv", "mp4", "flv", "mpeg", "mov", "ts", "m2ts", "wmv", "rm", "rmvb", "ogm", "webm"]
AUDIO_FORMATS = ["mp3", "flc", "m4a", "aac", "ogg", "3gp", "amr", "ape", "mka", "opus", "wavpack", "musepack"]

FORMATS = IMAGE_FORMATS + VIDEO_FORMATS + AUDIO_FORMATS

ALL_FILTER = "All ({})".format(" ".join(["*.{}".format(e) for e in IMAGE_FORMATS + VIDEO_FORMATS + AUDIO_FORMATS]))
IMAGE_FILTER = "Images ({})".format(" ".join(["*.{}".format(e) for e in IMAGE_FORMATS]))
VIDEO_FILTER = "Videos ({})".format(" ".join(["*.{}".format(e) for e in VIDEO_FORMATS]))
AUDIO_FILTER = "Audios ({})".format(" ".join(["*.{}".format(e) for e in AUDIO_FORMATS]))

VERSION = "0.0.1"
REVISION = "0"


class FILE_FORMAT(Enum):
    IMAGE = 0,
    VIDEO = 1,
    AUDIO = 2,
    URL = 3,
    INVALID = 4,


def get_dir_files(path):
    return [f for f in listdir(path) if isfile(join(path, f)) and get_extension(f) in FORMATS]


def get_file_ext(path):
    return split(path)[1]


def get_extension(filename):
    _, extension = splitext(filename)
    return extension[1:] if extension else ""


def get_format(filename):
    ext = get_extension(filename)
    if ext in IMAGE_FORMATS:
        return FILE_FORMAT.IMAGE
    elif ext in VIDEO_FORMATS:
        return FILE_FORMAT.VIDEO
    elif ext in AUDIO_FORMATS:
        return FILE_FORMAT.AUDIO
    return FILE_FORMAT.INVALID


def chunk(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


class URLValidator(QValidator):
    def __init__(self):
        super().__init__()
        regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        self.validator = QRegularExpressionValidator(QRegularExpression(regex))

    def validate(self, input, pos):
        return self.validator.validate(input, pos)
