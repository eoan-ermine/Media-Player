from PyQt5.QtCore import QUrl, QIODevice, QFile, QDataStream, QVariant, QTimer
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer, QAudioProbe, QAudio, QAudioDeviceInfo, \
    QAudioOutputSelectorControl, QMediaService

from src.database.database_manager import RecentFilesManager
from src.util.playlist_item import PlaylistItemDataRole
from src.util.utils import *
from src.gui.ui_manager import UIManager

from src.util.utils import get_format, FILE_FORMAT


class InputManager:
    __instance = None

    def __init__(self):
        if not InputManager.__instance:
            self.ui_manager = UIManager.get_instance()

            self.player = None
            self.playlist = None
            self.probe = None

            self.load_state()

            if not self.playlist:
                self.init_state()

            self.init_signals()

    def init_signals(self):
        self.player.durationChanged.connect(self.duration_changed_slot)
        self.player.positionChanged.connect(self.position_changed_slot)
        self.player.currentMediaChanged.connect(self.current_media_changed_slot)

        self.player.stateChanged.connect(self.state_changed_slot)

    def set_position(self, new_pos):
        self.ui_manager.set_position_slider_value(new_pos)
        self.player.setPosition(new_pos)

    def get_duration(self):
        return self.player.duration()

    def get_position(self):
        return self.player.position()

    def duration_changed_slot(self, duration):
        self.ui_manager.set_position_slider_max_value(duration)

    def position_changed_slot(self, position):
        self.ui_manager.set_position_slider_value(position)

    def get_volume(self):
        return self.player.volume()

    def set_volume(self, value):
        self.ui_manager.set_volume_slider_value(value)
        self.player.setVolume(value)

    def current_media_changed_slot(self):
        self.ui_manager.sync_row(self.get_media_position())

    def state_changed_slot(self, new_state):
        if new_state == QMediaPlayer.StoppedState or new_state == QMediaPlayer.PausedState:
            self.ui_manager.change_play_btn_state(False)
        else:
            self.ui_manager.change_play_btn_state(True)

    def next_media(self):
        self.playlist.next()

    def previous_media(self):
        self.playlist.previous()

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = InputManager(*args, **kwargs)
        return cls.__instance

    def init_state(self):
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        self.probe = QAudioProbe()
        self.probe.setSource(self.player)
        self.probe_connected = False

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)

        self.recent_files_manager = RecentFilesManager()

        self.ui_manager.set_output(self.player)
        self.player.setPlaylist(self.playlist)

    def load_state(self):
        file = QFile("file.dat")
        file.open(QIODevice.ReadOnly)
        in_stream = QDataStream(file)

        cur_playlist = QVariant()

        in_stream >> cur_playlist

        self.playlist = cur_playlist.value()

    def save_state(self):
        file = QFile("file.dat")
        file.open(QIODevice.WriteOnly)
        out = QDataStream(file)

        out << QVariant(self.current_playlist)

    def add_folder(self, path: str):
        files = get_dir_files(path)
        for file in files:
            self.add_media(path + "/" + file, get_format(file))

    def add_file(self, filename: str):
        format = get_format(filename)
        if format != FILE_FORMAT.INVALID:
            return self.add_media(filename, format)
        raise RuntimeError("Invalid file format")

    def add_media(self, filename: str, format: FILE_FORMAT):
        url = QUrl.fromLocalFile(filename)

        self.ui_manager.append_playlist(url.fileName(), format)

        self.recent_files_manager.write_recent_file(url.path())
        self.ui_manager.init_recent_files()

        self.playlist.addMedia(QMediaContent(url))

    def set_media_position(self, pos):
        self.playlist.setCurrentIndex(pos)

    def get_media_position(self):
        return self.playlist.currentIndex()

    def get_current_format(self):
        position = self.get_media_position()
        if position == -1:
            return None
        item = self.ui_manager.get_list_item(self.get_media_position())
        return item.data(PlaylistItemDataRole.FORMAT)

    def play(self):
        format = self.get_current_format()
        if format is None:
            return
        self.ui_manager.change_play_btn_state(True)
        if format == FILE_FORMAT.AUDIO:
            self.probe.audioBufferProbed.connect(self.process_buffer)
            self.probe_connected = True
        else:
            self.probe_connected = False
            self.ui_manager.show_video()
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def is_muted(self):
        return self.player.isMuted()

    def is_paused(self):
        return self.player.state() in (QMediaPlayer.StoppedState, QMediaPlayer.PausedState)

    def mute(self, toggle):
        self.ui_manager.change_mute_state(toggle, self.get_volume())
        self.player.setMuted(toggle)

    def get_playback_rate(self):
        return self.player.playbackRate()

    def set_playback_rate(self, value):
        self.player.setPlaybackRate(value)

    def process_buffer(self, buffer):
        if not self.probe_connected:
            return
        if not self.timer.isActive():
            self.timer.start()
        else:
            if self.timer.remainingTime() == 0:
                data = buffer.data()
                chunked = chunk(list(data.asarray(buffer.byteCount())), 12)

                to_visualizer = [int(sum(e) // 12 // 75) for e in chunked]

                self.show_visualization(to_visualizer)

    def show_visualization(self, to_visualizer):
        self.ui_manager.update_equalizer(to_visualizer)

    def get_audio_devices(self):
        return QAudioDeviceInfo.availableDevices(QAudio.AudioOutput)

    def get_recent_files(self):
        return self.recent_files_manager.get_recent_files()

    def clear_recent_files(self):
        return self.recent_files_manager.clear_recent_files()