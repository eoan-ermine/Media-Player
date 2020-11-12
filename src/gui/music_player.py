from PyQt5 import uic
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QLabel, QSizePolicy

from src.util import ImageViewer
from src.gui.input_manager import InputManager
from src.gui.dialogues import *


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../midi.ui", self)

        self.init_signals()
        self.init_ui()

        self.input_manager = InputManager.get_instance(self)
        self.installEventFilter(self)

        self.current_pixmap = None

    def init_ui(self):
        self.image_label = ImageViewer.ImageViewer()
        self.video_widget = QVideoWidget()

        self.stacked_widget.addWidget(self.video_widget)
        self.stacked_widget.addWidget(self.image_label)

    def init_signals(self):
        self.open_file_action.triggered.connect(lambda _: open_file_dialog())
        self.open_files_action.triggered.connect(lambda _: open_files_dialog())
        self.open_directory_action.triggered.connect(lambda _: open_directory_dialog())

    def set_image(self, filename: str):
        self.image_label.load_file(filename)
        self.image_label.fit_to_window()

    def show_image(self):
        self.stacked_widget.setCurrentWidget(self.image_label)

    def set_output(self, player):
        player.setVideoOutput(self.video_widget)

    def show_video(self):
        self.video_widget.show()
        self.stacked_widget.setCurrentWidget(self.video_widget)
