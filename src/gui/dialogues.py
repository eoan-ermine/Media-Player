from PyQt5 import uic
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QDialog, QFileDialog, QMenu
from PyQt5.QtCore import Qt, QTime

from src.radio.catalog_ui.radio_table_widget_item import QRadioTableWidgetItem
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


class PlaylistDialogPage(Enum):
    PLAYLIST = 0,
    LIBRARY = 1,

    VIDEO = 3,
    MUSIC = 4,
    PICTURE = 5,

    DISK = 7,

    PODCAST = 9,
    RADIO = 10,


class PlaylistDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.init_ui()
        self.init_signals()

        self.input_manager = InputManager().get_instance()
        self.current_page = PlaylistDialogPage.PLAYLIST

        self.draw_page(int(self.current_page))

    def init_ui(self):
        uic.loadUi("../playlist_dialog.ui", self)

    def draw_page(self, row):
        page = PlaylistDialogPage(row)

        self.media_table.clear()
        if page == PlaylistDialogPage.PLAYLIST:
            self.draw_playlist_page()
        elif page == PlaylistDialogPage.LIBRARY:
            self.draw_library_page()

        elif page == PlaylistDialogPage.VIDEO:
            self.draw_video_page()
        elif page == PlaylistDialogPage.MUSIC:
            self.draw_video_page()
        elif page == PlaylistDialogPage.PICTURE:
            self.draw_picture_page()

        elif page == PlaylistDialogPage.DISK:
            self.draw_disk_page()

        elif page == PlaylistDialogPage.PODCAST:
            self.draw_podcast_page()
        elif page == PlaylistDialogPage.RADIO:
            self.draw_radio_page()

    def open_media(self, row):
        item = self.media_table.itemAt(row, 0)
        if self.current_page == PlaylistDialogPage.RADIO:
            self.input_manager.add_media(item.url(), FILE_FORMAT.URL)
        self.input_manager.play()

    def draw_radio_page(self):
        stations = self.input_manager.get_radio_stations()
        for station in stations:
            item = QRadioTableWidgetItem(f"{station['name']}", url=station["stream_url"])
            self.media_table.setItem(self.media_table.rowCount(), 0, item)

    def init_signals(self):
        self.chooser.clicked.connect(
            lambda index: self.draw_page(index.row)
        )
        self.media_table.clicked.connect(
            lambda index: self.open_media(index.row)
        )
