from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import settingsWindow, testWindow
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import sqlite3
class HallsSettingsWindow(QMainWindow):
    def __init__(self, cinema_id, cinemaSettingsWindow):
        super().__init__()
        uic.loadUi('windows/halls_settings.ui', self)  
        self.cinema_id = cinema_id
        self.cinemaSettingsWindow = cinemaSettingsWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_4.clicked.connect(self.back)
        self.refresh()
    
    def back(self):
        self.cinemaSettingsWindow.show()
        self.close()

    def add(self):
        self.cur.execute(f"""INSERT INTO halls(hall, cinema_id) VALUES('{self.lineEdit.text()}', {self.cinema_id})""").fetchall()
        self.refresh()


    def find(self):
        # при пустой строке показывется весь список
        if self.lineEdit.text() == '':
            self.refresh()
            return
        # находим значения по названию кинотеатра
        result = self.cur.execute("SELECT * FROM halls WHERE hall=? and cinema_id=?",
                         (self.lineEdit.text(), self.cinema_id)).fetchall()
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
            self.cur.execute(f"DELETE FROM halls WHERE id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
        # обновление таблицы
        self.refresh()


    def select(self):
        if 0 < len(self.tableWidget.selectedItems()) <= 1:
            pass

    
    def refresh(self):
        result = self.cur.execute("""SELECT * FROM halls
            """).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()