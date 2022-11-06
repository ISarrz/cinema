from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import settingsWindow, testWindow
class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/test.ui', self) 