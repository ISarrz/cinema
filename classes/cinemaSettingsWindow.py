from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic

import sqlite3


class CinemaSettingsWindow(QMainWindow):
    def __init__(self, settingsWindow):
        super().__init__()
        uic.loadUi('windows/sinema_settings.ui', self) 
        self.settingsWindow = settingsWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_4.clicked.connect(self.back)
        self.refresh()
    
    def back(self):
        pass
        self.settingsWindow.show()
        self.hide()

    def add(self):
        self.cur.execute(f"""INSERT INTO cinemas(cinema) VALUES('{self.lineEdit.text()}')""").fetchall()
        self.refresh()


    def find(self):
        pass

    def delete(self):
        if 0 < len(self.tableWidget.selectedItems()) <= 1:
            self.cur.execute(f"DELETE FROM cinemas WHERE id={self.tableWidget.selectedItems()[0].text()}")
        self.refresh()


    def select(self):
        pass
    
    def refresh(self):
        result = self.cur.execute("""SELECT * FROM cinemas
            """).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()