from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt

from src.util.utils import *
from src.gui.input_manager import InputManager


def open_file_dialog(hint="Select file to open", dir="", filter=";;".join([IMAGE_FILTER, VIDEO_FILTER, AUDIO_FILTER])):
    filename, _ = QFileDialog.getOpenFileName(None, hint, dir, filter)
    if filename:
        InputManager.get_instance().add_file(filename, get_format(filename))


def open_files_dialog() -> [str]:
    dialog = OpenFilesDialog()
    dialog.exec_()


def open_directory_dialog(hint="Select directory to open", dir="", options=QFileDialog.ShowDirsOnly):
    directory = QFileDialog.getExistingDirectory(None, hint, dir, options)
    if directory:
        InputManager.get_instance().add_folder(directory)


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
        self.file_browse_button.clicked.connect()
        self.cancel_btn.clicked.connect(lambda: self.done(0))