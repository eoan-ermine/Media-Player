from PyQt5 import uic
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow

from src.util import ImageViewer
from src.util.utils import *

from src.gui.ui_manager import UIManager
from src.gui.input_manager import InputManager
from src.gui.dialogues import *


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../midi.ui", self)

        self.init_signals()
        self.init_ui()

        self.ui_manager = UIManager.get_instance(self)
        self.input_manager = InputManager.get_instance()

        self.installEventFilter(self)

        self.current_pixmap = None

    def init_ui(self):
        self.image_label = ImageViewer.ImageViewer()
        self.video_widget = QVideoWidget()

        self.stacked_widget.addWidget(self.video_widget)
        self.stacked_widget.addWidget(self.image_label)

    def init_signals(self):
        self.open_file_action.triggered.connect(self.open_file_action_slot)
        self.open_files_action.triggered.connect(self.open_files_action_slot)
        self.open_directory_action.triggered.connect(self.open_directory_action_slot)

    @staticmethod
    def open_file_action_slot():
        open_file_dialog()

    @staticmethod
    def open_files_action_slot():
        open_files_dialog()

    @staticmethod
    def open_directory_action_slot():
        open_directory_dialog()
