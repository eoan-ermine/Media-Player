from PyQt5.QtCore import QUrl, QIODevice, QFile, QDataStream, QVariant, QTimer
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer, QAudioProbe

from src.util.utils import *
from src.gui.ui_manager import UIManager


class InputManager:
    __instance = None

    def __init__(self):
        if not InputManager.__instance:
            self.ui_manager = UIManager.get_instance()

            self.player = None
            self.playlist = None
            self.probe = None

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

        self.probe = QAudioProbe()
        self.probe.setSource(self.player)

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)

        self.ui_manager.set_output(self.player)
        self.player.setPlaylist(self.playlist)

        self.probe.audioBufferProbed.connect(self.process_buffer)

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
        if format != FILE_FORMAT.INVALID:
            self.add_media(filename)
            if format == FILE_FORMAT.AUDIO:
                self.add_media(filename)
                self.show_visualization()

    def add_media(self, filename: str):
        url = QUrl.fromLocalFile(filename)

        self.playlist.addMedia(QMediaContent(url))
        self.ui_manager.append_playlist(url.fileName())

    def play(self):
        self.ui_manager.show_video()
        self.player.play()

    def process_buffer(self, buffer):
        if not self.timer.isActive():
            self.timer.start()
        else:
            if self.timer.remainingTime() == 0:
                data = buffer.data()
                chunked = chunk(list(data.asarray(buffer.byteCount())), 12)

                to_visualizer = [int(sum(e) // 12 // 75) for e in chunked]

                self.show_visualization(to_visualizer)

    def show_visualization(self, to_visualizer):
        self.ui_manager.update_equalizer(to_visualizer)