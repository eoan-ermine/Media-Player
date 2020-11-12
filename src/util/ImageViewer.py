from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImageReader, QPalette, QImage, QColorSpace, QPixmap
from PyQt5.QtWidgets import QScrollArea, QMessageBox, QSizePolicy, QLabel


class ImageViewer(QScrollArea):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel()
        self.image = QImage()

        self.image_label.setBackgroundRole(QPalette.Base)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(True)

        self.setBackgroundRole(QPalette.Dark)
        self.setWidget(self.image_label)
        self.setVisible(False)

        self.scale_factor = 1.0

    def load_file(self, filename):
        reader = QImageReader(filename)
        new_image = reader.read()

        if new_image.isNull():
            return False

        self.set_image(new_image)

        return True

    def set_image(self, new_image):
        self.image = new_image
        if self.image.colorSpace().isValid():
            self.image.convertToColorSpace(QColorSpace(QColorSpace.SRgb))
        self.image_label.setPixmap(QPixmap.fromImage(self.image))
        self.scale_factor = 1.0

        self.setVisible(True)

    def zoom_in(self):
        self.scale_image(1.25)

    def zoom_out(self):
        self.scale_image(0.8)

    def normal_size(self):
        self.image_label.adjustSize()
        self.scale_factor = 1.0

    def fit_to_window(self):
        self.setWidgetResizable(True)

    def scale_image(self, factor):
        self.scale_factor *= factor
        self.image_label.resize(self.scale_factor * self.image_label.pixmap(Qt.ReturnByValue).size())