import sys
from PyQt5.QtWidgets import QApplication
from classes import startWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = startWindow.StartWindow()
    ex.show()
    sys.exit(app.exec_())