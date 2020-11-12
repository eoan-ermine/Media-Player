from enum import IntEnum

from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtWidgets import QListWidgetItem


class PlaylistItemDataRole(IntEnum):
    PATH = 256,


class PlaylistItem(QListWidgetItem):
    def __init__(self, path, alias):
        super(QListWidgetItem, self).__init__(alias)

        self.setData(PlaylistItemDataRole.PATH, QVariant(path))