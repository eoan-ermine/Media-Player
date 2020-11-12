from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt5.QtGui import QPainter, QIcon, QBrush, QColor,\
    QLinearGradient, QPaintEvent, QPen
from PyQt5.QtWidgets import QWidget,\
    QStyleOptionToolButton, QToolButton, QStyle
from PyQt5.QtCore import QSize


class RoundButton(QToolButton):
    def __init__(self, parent: QWidget):
        QToolButton.__init__(self, parent)

        self.setIconSize(QSize(24, 24))
        self.setIcon(QIcon("icons/media-playback-start.svg"))

    def sizeHint(self) -> QSize:
        return QSize(38, 38)

    def pen(self, option: QStyleOptionToolButton) -> QBrush:
        over = option.state & QStyle.State_MouseOver
        return QBrush(QColor(61, 165, 225) if over else QColor(109, 106, 102))

    def brush(self, option: QStyleOptionToolButton):
        over = option.state & QStyle.State_MouseOver
        pressed = option.state & QStyle.State_Sunken

        g1 = QColor(219, 217, 215)
        g2 = QColor(205, 202, 199)
        g3 = QColor(187, 183, 180)

        if pressed:
            g1 = g1.darker(120)
            g2 = g2.darker(120)
            g3 = g3.darker(120)
        elif over:
            g1 = g1.lighter(110)
            g2 = g2.lighter(110)
            g3 = g3.lighter(110)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, g1)
        gradient.setColorAt(0.40, g2)
        gradient.setColorAt(1.0, g3)

        return QBrush(gradient)

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)

        option = QStyleOptionToolButton()

        self.initStyleOption(option)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(self.pen(option), 1.5))
        painter.setBrush(self.brush(option))
        painter.drawEllipse(self.rect().adjusted(1, 1, -1, -1));

        self.style().drawControl(QStyle.CE_ToolButtonLabel, option, painter, self)