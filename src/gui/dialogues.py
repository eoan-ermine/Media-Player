from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt


def open_file_dialog(hint="Select file to open", dir="", filter="") -> (str, str):
    filename, type = QFileDialog.getOpenFileName(None, hint, dir, filter)
    return filename, type


def open_files_dialog(hint="Select one or multiple files to open", dir="", filter="") -> (str, str):
    filenames, type = QFileDialog.getOpenFileNames(None, hint, dir, filter)
    return filenames, type


def open_directory_dialog(hint="Select directory to open", dir="", options=QFileDialog.ShowDirsOnly):
    directory = QFileDialog.getExistingDirectory(None, hint, dir, options)
    return directory


# Already implemented: Close Button
# TODO: Add btn, Remove btn, Browse subtitles btn, Play btn
class OpenFilesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.init_ui()

        self.init_signals()

    def init_ui(self):
        uic.loadUi("../open_file_dialog.ui", self)

    def init_signals(self):
        self.cancel_btn.clicked.connect(lambda: self.done(0))
