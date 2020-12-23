from enum import Enum, auto

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem


class RadioTableWidgetItemRole(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return Qt.UserRole + count
    URL = auto()


class QRadioTableWidgetItem(QTableWidgetItem):
    def __init__(self, *args, url, **kwargs):
        super().__init__(*args, **kwargs)
        self.setData(RadioTableWidgetItemRole.URL, url)

    def set_url(self, url):
        self.setData(RadioTableWidgetItemRole.URL, url)

    def url(self):
        return self.data(RadioTableWidgetItemRole.URL)
