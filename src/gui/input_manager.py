from PyQt5.QtCore import QUrl, QIODevice, QFile, QDataStream, QVariant
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer

import time


class InputManager:
    __instance = None

    def __init__(self, parent):
        if not InputManager.__instance:
            self.parent = parent

            self.player = None
            self.playlist = None

            self.load_state()

            if not self.playlist:
                self.init_state()

    @classmethod
    def get_instance(cls, parent):
        if not cls.__instance:
            cls.__instance = InputManager(parent)
        return cls.__instance

    def init_state(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        self.parent.set_output(self.player)
        self.player.setPlaylist(self.playlist)

    def load_state(self):
        file = QFile("file.dat")
        file.open(QIODevice.ReadOnly)
        in_stream = QDataStream(file)

        cur_playlist = QVariant()

        in_stream >> cur_playlist

        self.playlist = cur_playlist.value()

    def save_state(self):
        file = QFile("file.dat")
        file.open(QIODevice.WriteOnly)
        out = QDataStream(file)

        out << QVariant(self.current_playlist)

    def show_image(self, filename):
        self.parent.set_image(filename)
        self.parent.show_image()

    def add_video(self, filename):
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(filename)))

    def play_video(self):
        self.parent.show_video()
        self.player.play()
