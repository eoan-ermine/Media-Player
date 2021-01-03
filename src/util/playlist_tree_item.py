from PyQt5.QtWidgets import QTreeWidgetItem


class PlaylistTreeItem(QTreeWidgetItem):
    def __init__(self, text, parent=None):
        super(QTreeWidgetItem, self).__init__(parent)
        self.setText(0, text)
