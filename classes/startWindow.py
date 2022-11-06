from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import settingsWindow, testWindow

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/start_window.ui', self) 
        self.pushButton.clicked.connect(self.next)

        self.settingsWindow = settingsWindow.SettingsWindow()
    def next(self):

        testWindow.TestWindow().show()
        self.hide()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.AltModifier + Qt.ShiftModifier):
         if event.key() == Qt.Key_Q:
            self.settingsWindow.show()
            self.hide()