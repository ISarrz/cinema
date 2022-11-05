import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/start_window.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.next)
        self.testWindow = TestWindow()
    def next(self):
        self.testWindow.show()
        self.hide()
        # Обратите внимание: имя элемента такое же как в QTDesigner

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/test.ui', self)  # Загружаем дизайн
        
    def next(self):
        self.nextCH = True
        # Обратите внимание: имя элемента такое же как в QTDesigner


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.exit(app.exec_())