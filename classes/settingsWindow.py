from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import cinemaSettingsWindow, settingsWindow, testWindow
class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/settings.ui', self)  
        self.cinemaSettings = cinemaSettingsWindow.CinemaSettingsWindow(self)
        self.pushButton.clicked.connect(self.cinema_settings)
        self.pushButton_2.clicked.connect(self.movie_settings)

    def cinema_settings(self):
        self.close()
        self.cinemaSettings.show()

    def movie_settings(self):
        pass