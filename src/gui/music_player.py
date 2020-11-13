from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, qApp

from src.util.equalizer_bar import EqualizerBar
from src.util.utils import *

from src.gui.ui_manager import UIManager
from src.gui.input_manager import InputManager
from src.gui.dialogues import *

from src.util.round_button import RoundButton


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../midi.ui", self)

        self.init_ui()
        self.init_signals()

        self.ui_manager = UIManager.get_instance(self)
        self.input_manager = InputManager.get_instance()

        self.installEventFilter(self)

        self.current_pixmap = None

    def init_ui(self):
        self.stacked_widget = QStackedWidget()

        self.video_widget = QVideoWidget()
        self.stacked_widget.addWidget(self.video_widget)

        self.content_layout.addWidget(self.stacked_widget)

        self.equalizer = EqualizerBar(12, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                          '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])
        self.equalizer.show()

        self.button = RoundButton(self)
        self.button.setCheckable(True)
        self.button.setIcon(QIcon(":/play_icon"))

        self.buttons_layout.insertWidget(6, self.button)
        self.stacked_widget.addWidget(self.equalizer)

    def init_signals(self):
        self.open_file_action.triggered.connect(self.open_file_action_slot)
        self.open_files_action.triggered.connect(self.open_files_action_slot)
        self.open_directory_action.triggered.connect(self.open_directory_action_slot)

        self.list_widget.currentRowChanged.connect(self.row_changed_slot)

        self.position_slider.sliderMoved.connect(self.position_slider_moved)
        self.volume_slider.sliderMoved.connect(self.volume_slider_moved)

        self.stop_btn.clicked.connect(self.stop_slot)
        self.skip_backward_btn.clicked.connect(self.skip_backward_slot)
        self.button.toggled.connect(self.on_play_slot)
        self.skip_forward_btn.clicked.connect(self.skip_forward_slot)

        self.about_qt.triggered.connect(lambda: qApp.aboutQt())
        self.about_app.triggered.connect(lambda: AboutDialog().exec_())

    @staticmethod
    def open_file_action_slot():
        open_file_dialog()

    @staticmethod
    def open_files_action_slot():
        open_files_dialog()

    @staticmethod
    def open_directory_action_slot():
        open_directory_dialog()

    def row_changed_slot(self, current_row):
        if current_row < 0:
            return

        self.input_manager.set_media_position(current_row)
        self.input_manager.play()

    def on_play_slot(self, checked):
        self.ui_manager.change_play_icon(checked)
        if checked:
            self.input_manager.play()
        else:
            self.input_manager.pause()

    def position_slider_moved(self, value):
        self.input_manager.set_position(value)

    def volume_slider_moved(self, value):
        self.input_manager.set_volume(value)

    def skip_backward_slot(self):
        self.input_manager.previous_media()

    def skip_forward_slot(self):
        self.input_manager.next_media()

    def stop_slot(self):
        self.input_manager.stop()