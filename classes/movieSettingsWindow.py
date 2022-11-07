from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import settingsWindow, testWindow
class MovieSettingsWindow(QMainWindow):
    def __init__(self):
        uic.loadUi('windows/settings.ui', self)  


