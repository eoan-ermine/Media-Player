from abc import ABC
from PyQt5.QtGui import QPalette, QFont


class AbstractModel(ABC):
    @property
    def list_widget_palette(self) -> QPalette:
        raise NotImplementedError()
    
    @property
    def menu_palette(self) -> QPalette:
        raise NotImplementedError()

    @property
    def menu_label_font(self) -> QFont:
        raise NotImplementedError()

    @property
    def menu_items_font(self) -> QFont:
        raise NotImplementedError()
