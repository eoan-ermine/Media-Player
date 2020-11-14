from PyQt5.QtGui import QIcon

from src.util import playlist_item
from src.util.utils import *

import random


class UIManager:
    __instance = None

    def __init__(self, parent=None):
        if not UIManager.__instance:
            self.parent = parent

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = UIManager(*args, **kwargs)
        return cls.__instance

    def set_output(self, player):
        player.setVideoOutput(self.parent.video_widget)

    def show_video(self):
        if self.parent.stacked_widget.currentWidget() != self.parent.video_widget:
            self.parent.stacked_widget.setCurrentWidget(self.parent.video_widget)

    def append_playlist(self, element, format):
        self.parent.list_widget.addItem(playlist_item.PlaylistItem(element, get_file_ext(element), format))

    def show_equalizer(self):
        if self.parent.stacked_widget.currentWidget() != self.parent.equalizer:
            self.parent.stacked_widget.setCurrentWidget(self.parent.equalizer)

    def update_equalizer(self, data):
        self.show_equalizer()
        self.parent.equalizer.setValues([min(100, e+random.randint(0, 50) if random.randint(0, 5) > 2 else e) for e in data])

    def change_play_icon(self, checked):
        self.parent.button.setIcon(QIcon(":/pause_icon") if checked else QIcon(":/play_icon"))

    def change_play_btn_state(self, state):
        self.parent.pause_action.setText("Пауза" if state else "Воспроизвести")
        self.parent.button.setChecked(state)

    def change_mute_state(self, state, last_volume):
        self.parent.mute_action.setText("Включить звук" if state else "Выключить звук")

        self.parent.volume_slider.setEnabled(not state)
        self.set_volume_slider_value(0 if state else last_volume)

    def get_list_item(self, idx):
        return self.parent.list_widget.item(idx)

    def sync_row(self, sync_value):
        self.parent.list_widget.setCurrentRow(sync_value)

    def set_position_slider_value(self, value):
        self.parent.position_slider.setValue(value)

    def set_position_slider_max_value(self, value):
        self.parent.position_slider.setMaximum(value)

    def set_volume_slider_value(self, value):
        self.parent.volume_slider.setValue(value)