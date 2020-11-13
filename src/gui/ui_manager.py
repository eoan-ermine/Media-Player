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
        self.parent.video_widget.show()

    def append_playlist(self, element):
        self.parent.list_widget.addItem(PlaylistWidgetItem.PlaylistItem(element, get_file_ext(element)))

    def show_equalizer(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.equalizer)

    def update_equalizer(self, data):
        if self.parent.stacked_widget.currentWidget() != self.parent.equalizer:
            self.show_equalizer()
        self.parent.equalizer.setValues([min(100, e+random.randint(0, 50) if random.randint(0, 5) > 2 else e) for e in data])