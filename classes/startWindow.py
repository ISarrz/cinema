from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt
from classes import settingsWindow, testWindow, filmsBuyWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/start_window.ui', self) 
        self.setWindowIcon(QtGui.QIcon("img/icon.png"))
        self.pushButton.clicked.connect(self.next)
        self.settingsWindow = settingsWindow.SettingsWindow(self)
        self.filmsBuyWindow = filmsBuyWindow.FilmsBuyWindow(self)

    def next(self):
        self.filmsBuyWindow.show()
        self.close()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
         if event.key() == Qt.Key_Q:
            self.settingsWindow.show()
            self.close()
