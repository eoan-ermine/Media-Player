from PyQt5.QtCore import QUrl, QIODevice, QFile, QDataStream, QVariant
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer

from src.util.utils import *
from src.gui.ui_manager import UIManager


class InputManager:
    __instance = None

    def __init__(self):
        if not InputManager.__instance:
            self.ui_manager = UIManager.get_instance()

            self.player = None
            self.playlist = None

            self.load_state()

            if not self.playlist:
                self.init_state()

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = InputManager(*args, **kwargs)
        return cls.__instance

    def init_state(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        self.ui_manager.set_output(self.player)
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

    def add_folder(self, path: str):
        files = get_dir_files(path)
        for file in files:
            self.add_file(file, get_format(file))

    def add_file(self, filename: str, format: FILE_FORMAT):
        if format == FILE_FORMAT.IMAGE:
            self.show_image(filename)
        if format in (FILE_FORMAT.VIDEO, FILE_FORMAT.AUDIO):
            self.add_media(filename)

    def show_image(self, filename: str):
        self.ui_manager.append_playlist(filename)
        self.ui_manager.set_image(filename)
        self.ui_manager.show_image()

    def add_media(self, filename: str):
        url = QUrl.fromLocalFile(filename)

        self.playlist.addMedia(QMediaContent(url))
        self.ui_manager.append_playlist(url.fileName())

    def play_video(self):
        self.ui_manager.show_video()
        self.player.play()
