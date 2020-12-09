from PyQt5.QtGui import QPalette, QFont
from src.gui.customization.abstract_model import AbstractModel


class StandardModel(AbstractModel):
    def list_widget_palette(self) -> QPalette:
        return QPalette()

    def menu_palette(self) -> QPalette:
        return QPalette()

    def menu_label_font(self) -> QFont:
        return QFont()