from src.util import PlaylistWidgetItem
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
        self.parent.list_widget.addItem(PlaylistWidgetItem.PlaylistItem(element, get_file_ext(element), format))

    def show_equalizer(self):
        if self.parent.stacked_widget.currentWidget() != self.parent.equalizer:
            self.parent.stacked_widget.setCurrentWidget(self.parent.equalizer)

    def update_equalizer(self, data):
        self.show_equalizer()
        self.parent.equalizer.setValues([min(100, e+random.randint(0, 50) if random.randint(0, 5) > 2 else e) for e in data])