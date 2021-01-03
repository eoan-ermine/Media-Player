from PyQt5 import uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QFileDialog, QMenu
from PyQt5.QtCore import Qt, QTime

from src.radio.catalog_ui.radio_table_widget_item import QRadioTableWidgetItem
from src.util.playlist_tree_item import PlaylistTreeItem
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


def open_url_dialog():
    dialog = OpenURLDialog()
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


class OpenURLDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.init_ui()
        self.init_signals()

        self.input_manager = InputManager.get_instance()

    def init_ui(self):
        uic.loadUi("../open_url_dialog.ui", self)

        menu = QMenu()
        menu.addAction("Добавить в очередь", lambda: [self.push_to_queue(), self.done(0)], QKeySequence("Alt+E"))
        menu.addAction("Воспроизвести", lambda: [self.push_to_play(), self.done(0)], QKeySequence("Alt+P"))
        self.play_btn.setMenu(menu)

        self.url_edit.setValidator(URLValidator())

    def init_signals(self):
        self.cancel_btn.clicked.connect(lambda: self.done(-1))

    def push_to_queue(self):
        self.input_manager.add_media(self.url_edit.text(), FILE_FORMAT.URL)

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


def open_playlist_dialog():
    dialog = PlaylistDialog()
    dialog.exec_()


class PlaylistDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.input_manager = InputManager().get_instance()
        self.radio_categories = []

        self.init_ui()
        self.init_signals()

        self.current_page = None

    def init_ui(self):
        uic.loadUi("../playlist_dialog.ui", self)

        self.playlist_item = PlaylistTreeItem("Плейлист", self.chooser)
        self.mediateque_item = PlaylistTreeItem("Медиатека", self.chooser)

        self.computer_item = PlaylistTreeItem("Компьютер", self.chooser)

        self.video_item = PlaylistTreeItem("Видео", self.computer_item)
        self.music_item = PlaylistTreeItem("Музыка", self.computer_item)
        self.pictures_item = PlaylistTreeItem("Изображения", self.computer_item)

        self.devices_item = PlaylistTreeItem("Устройства", self.chooser)
        self.disks_item = PlaylistTreeItem("Диски", self.devices_item)

        self.internet_item = PlaylistTreeItem("Интернет", self.chooser)
        self.podcasts_item = PlaylistTreeItem("Подкасты", self.internet_item)

        self.radio_item = PlaylistTreeItem("Радио", self.internet_item)
        for category in self.input_manager.get_radio_categories():
            self.radio_categories.append(
                PlaylistTreeItem(category["name"], self.radio_item)
            )

    def draw_page(self, item):
        self.current_page = item

        if item == self.radio_item:
            self.draw_radio_page()
        if item in self.radio_categories:
            self.draw_radio_page(category=item.text(0))

    def open_media(self, item):
        if self.current_page == self.radio_item or self.current_page in self.radio_categories:
            self.input_manager.add_media(item.url(), FILE_FORMAT.URL)
        self.input_manager.play()

    def draw_radio_page(self, category=None):
        if not category:
            stations = self.input_manager.get_radio_stations(limit=50)
        else:
            stations = self.input_manager.get_radio_stations(limit=50, category=category)
        self.media_table.setRowCount(len(stations))
        for i, station in enumerate(stations):
            item = QRadioTableWidgetItem(f"{station['name']}", url=station["stream_url"])
            self.media_table.setItem(i, 0, item)

    def init_signals(self):
        self.chooser.itemActivated.connect(self.draw_page)
        self.media_table.itemDoubleClicked.connect(self.open_media)
