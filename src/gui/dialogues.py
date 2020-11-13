from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt

from src.util.utils import *
from src.gui.input_manager import InputManager


def open_file_dialog(hint="Select file to open", dir="", filter=";;".join([IMAGE_FILTER, VIDEO_FILTER, AUDIO_FILTER]),
                     process=lambda k: InputManager.get_instance().add_file(k, get_format(k))):
    filename, _ = QFileDialog.getOpenFileName(None, hint, dir, filter)
    if filename:
        process(filename)


def open_files_dialog():
    dialog = OpenFilesDialog()
    dialog.exec_()


def open_directory_dialog(hint="Select directory to open", dir="", options=QFileDialog.ShowDirsOnly,
                          process=lambda k: InputManager.get_instance().add_folder(k)):
    directory = QFileDialog.getExistingDirectory(None, hint, dir, options)
    if directory:
        process(directory)


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