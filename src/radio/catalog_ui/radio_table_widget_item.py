from PyQt5.QtWidgets import QTableWidgetItem


class QRadioWidgetItem(QTableWidgetItem):
    def __init__(self, *args, url, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url

    def set_url(self, url):
        self.url = url

    def url(self):
        return self.url
