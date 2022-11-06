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
        self.settingsWindow.show()
        self.hide()

    def add(self):
        self.cur.execute(f"""INSERT INTO cinemas(cinema) VALUES('{self.lineEdit.text()}')""").fetchall()
        self.refresh()


    def find(self):
        # при пустой строке показывется весь список
        if self.lineEdit.text() == '':
            self.refresh()
            return
        # находим значения по названию кинотеатра
        result = self.cur.execute("SELECT * FROM cinemas WHERE cinema=?",
                         (self.lineEdit.text(), )).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def delete(self):
        if 0 < len(self.tableWidget.selectedItems()):
            # удаление выделенных id 
            ids = [i.text() for i in self.tableWidget.selectedItems()]
            self.cur.execute(f"DELETE FROM cinemas WHERE id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
        # обновление таблицы
        self.refresh()


    def select(self):
        if 0 < len(self.tableWidget.selectedItems()) <= 1:
            pass

    
    def refresh(self):
        result = self.cur.execute("""SELECT * FROM cinemas
            """).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()