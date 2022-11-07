from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import cinemaSettingsWindow, filmsSettingsWindow
class SettingsWindow(QMainWindow):
    def __init__(self, startWindow):
        super().__init__()
        uic.loadUi('windows/settings.ui', self)  
        self.cinemaSettings = cinemaSettingsWindow.CinemaSettingsWindow(self)
        self.filmsSettings = filmsSettingsWindow.FilmsSettingsWindow(self)
        self.pushButton.clicked.connect(self.cinema_settings)
        self.pushButton_2.clicked.connect(self.movie_settings)
        self.startWindow = startWindow

    def cinema_settings(self):
        self.close()
        self.cinemaSettings.show()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.startWindow.show()
            self.close()

    def movie_settings(self):
        self.filmsSettings.show()
        self.close()