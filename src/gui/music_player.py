from PyQt5 import uic
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, qApp, QAction

from src.shells.abstract_shell import AbstractShell
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

        self.ui_manager = UIManager.get_instance(self)
        self.input_manager = None

        self.init_ui()
        self.init_signals()

        self.installEventFilter(self)

        self.current_pixmap = None
        AbstractShell("hello", "bye").show_intro()

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

        self.input_manager = InputManager.get_instance()

        self.audio_devices_menu = QMenu()
        for element in self.input_manager.get_audio_devices():
            if element.realm() != "default":
                continue
            self.audio_devices_menu.addAction(element.deviceName())
        self.audiodevice_action.setMenu(self.audio_devices_menu)

        self.init_recent_files()

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

        self.faster_action.triggered.connect(lambda: self.change_speed(0.5))
        self.bit_faster_action.triggered.connect(lambda: self.change_speed(0.25))
        self.normal_speed_action.triggered.connect(lambda: self.set_speed(1.0))
        self.bit_slower_action.triggered.connect(lambda: self.change_speed(-0.25))
        self.slower_action.triggered.connect(lambda: self.change_speed(-0.5))

        self.pause_action.triggered.connect(lambda: self.input_manager.play() if self.input_manager.is_paused()
                                            else self.input_manager.pause())

        self.forward_time_action.triggered.connect(lambda: self.time_travel(10))
        self.backward_time_action.triggered.connect(lambda: self.time_travel(-10))
        self.to_time_action.triggered.connect(lambda: self.open_time_travel_dialog_slot())

        self.stop_action.triggered.connect(lambda: self.input_manager.stop())
        self.previous_action.triggered.connect(self.skip_backward_slot)
        self.next_action.triggered.connect(self.skip_forward_slot)

        self.increase_volume_action.triggered.connect(lambda: self.change_volume(10))
        self.decrease_volume_action.triggered.connect(lambda: self.change_volume(-10))

        self.mute_action.triggered.connect(lambda: self.input_manager.mute(not self.input_manager.is_muted()))

        self.fullscreen_action.triggered.connect(lambda: self.showFullScreen() if not self.isFullScreen()
                                                 else self.showNormal())
        self.show_on_top_action.triggered.connect(lambda state: self.show_on_top(state))

        self.about_qt.triggered.connect(lambda: qApp.aboutQt())
        self.about_app.triggered.connect(lambda: AboutDialog().exec_())
        self.exit_action.triggered.connect(lambda: qApp.closeAllWindows())

    @staticmethod
    def open_file_action_slot():
        open_file_dialog()

    @staticmethod
    def open_files_action_slot():
        open_files_dialog()

    @staticmethod
    def open_directory_action_slot():
        open_directory_dialog()

    @staticmethod
    def open_time_travel_dialog_slot():
        open_time_travel_dialog()

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

    def set_speed(self, value):
        self.input_manager.set_playback_rate(value)

    def change_speed(self, delta):
        self.input_manager.set_playback_rate(self.input_manager.get_playback_rate() + delta)

    def change_volume(self, delta):
        self.input_manager.set_volume(self.input_manager.get_volume() + delta)

    def time_travel(self, seconds):
        self.input_manager.set_position(self.input_manager.get_position() + seconds * 1000)

    def show_on_top(self, state):
        self.ui_manager.show_on_top(state)

    def init_recent_files(self):
        recent_files = self.input_manager.get_recent_files()
        for path in recent_files:
            self.recent_files_menu.addAction(path, lambda: self.input_manager.add_media(
                QObject.sender().text()
            ))
        self.recent_files_menu.addSeparator()
        self.recent_files_menu.addAction(
            "Очистить",
            lambda: [self.input_manager.clear_recent_files(), self.init_recent_files()]
        )