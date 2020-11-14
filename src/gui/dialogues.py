from PyQt5 import uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QFileDialog, QMenu
from PyQt5.QtCore import Qt, QTime

from src.util.utils import *
from src.util.playlist_item import PlaylistItem, PlaylistItemDataRole

from src.gui.input_manager import InputManager


def open_file_dialog(hint="Select file to open", dir="", filter=";;".join([ALL_FILTER, IMAGE_FILTER,
                                                                           VIDEO_FILTER, AUDIO_FILTER]),
                     process=lambda k: InputManager.get_instance().add_media(k, get_format(k))):
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


def open_time_travel_dialog():
    dialog = TimeTravelDialog()
    dialog.exec_()


class OpenFilesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.init_ui()
        self.init_signals()

        self.input_manager = InputManager.get_instance()

    def init_ui(self):
        uic.loadUi("../open_file_dialog.ui", self)

        menu = QMenu()
        menu.addAction("Добавить в очередь", lambda: [self.push_to_queue(), self.done(0)], QKeySequence("Alt+E"))
        menu.addAction("Воспроизвести", lambda: [self.push_to_play(), self.done(0)], QKeySequence("Alt+P"))

        self.play_btn.setMenu(menu)

    def init_signals(self):
        self.file_list.currentItemChanged.connect(lambda p, c: self.remove_file_btn.setEnabled(True))

        self.file_browse_btn.clicked.connect(self.file_browse_slot)
        self.remove_file_btn.clicked.connect(self.remove_file_slot)

        self.cancel_btn.clicked.connect(lambda: self.done(-1))

    def file_browse_slot(self):
        open_file_dialog(process=lambda k: self.file_list.addItem(PlaylistItem(k, get_file_ext(k), get_format(k))))

    def remove_file_slot(self):
        self.file_list.takeItem(self.file_list.row(self.file_list.currentItem()))
        if self.file_list.count() == 0:
            self.remove_file_btn.setEnabled(False)

    def get_files_to_send(self):
        files = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            files.append((item.data(PlaylistItemDataRole.PATH), item.data(PlaylistItemDataRole.FORMAT)))
        return files

    def push_to_queue(self):
        for path, format in self.get_files_to_send():
            self.input_manager.add_media(path, format)

    def push_to_play(self):
        self.push_to_queue()
        self.input_manager.play()


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        uic.loadUi("../about_box.ui", self)

        self.version_label.setText("Version: {}".format(VERSION))
        self.revision_label.setText("Revision: {}".format(REVISION))

    def init_signals(self):
        self.buttonBox.accepted.connect(lambda: self.done(0))


class TimeTravelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.init_ui()
        self.init_signals()

        self.input_manager = InputManager().get_instance()

    def init_ui(self):
        uic.loadUi("../time_travel_dialog.ui", self)

    def init_signals(self):
        self.reset_btn.clicked.connect(lambda: self.time_edit.clear())

        self.go_btn.clicked.connect(self.go_btn_slot)
        self.cancel_btn.clicked.connect(lambda: self.done(-1))

    def go_btn_slot(self):
        new_position = QTime(0, 0).secsTo(self.time_edit.time()) * 1000
        self.input_manager.set_position(new_position)

        self.done(0)
