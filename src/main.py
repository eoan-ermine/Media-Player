import sys
import resources

from src.gui.music_player import MusicPlayer
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    music_player = MusicPlayer()
    music_player.show()

    sys.exit(app.exec_())