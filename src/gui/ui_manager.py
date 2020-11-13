from src.util import PlaylistWidgetItem
from src.util.utils import *


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

    def set_image(self, filename: str):
        self.parent.image_label.load_file(filename)
        self.parent.image_label.fit_to_window()

    def show_image(self):
        self.parent.stacked_widget.setCurrentWidget(self.parent.image_label)

    def set_output(self, player):
        player.setVideoOutput(self.parent.video_widget)

    def show_video(self):
        self.parent.video_widget.show()
        self.parent.stacked_widget.setCurrentWidget(self.parent.video_widget)

    def append_playlist(self, element):
        self.parent.list_widget.addItem(PlaylistWidgetItem.PlaylistItem(element, get_file_ext(element)))