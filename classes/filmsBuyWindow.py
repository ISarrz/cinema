from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import hallsSettingsWindow, cinemaBuyWindow
import sqlite3


class FilmsBuyWindow(QMainWindow):
    def __init__(self, startWindow):
        super().__init__()
        uic.loadUi('windows/films_buy.ui', self) 
        self.startWindow = startWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.film_id = 0
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_4.clicked.connect(self.back)
        self.refresh()
    
    def back(self):
        self.startWindow.show()
        self.close()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.startWindow.show()
            self.close()


    def find(self):
        # при пустой строке показывется весь список
        if self.lineEdit.text() == '':
            self.refresh()
            return
        # находим значения по названию кинотеатра
        result = self.cur.execute("SELECT * FROM films WHERE film=?",
                         (self.lineEdit.text(), )).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def select(self):
        
        if 0 < len(self.tableWidget.selectedItems()) <= 1:
            row = self.tableWidget.selectedItems()[0].row()
            self.film_id = self.tableWidget.takeItem(row, 0).text()
            self.cinemaBuyWindow = cinemaBuyWindow.CinemaBuyWindow(self)
            self.cinemaBuyWindow.show()
            self.cinemaBuyWindow.refresh()
            self.close()
            

    
    def refresh(self):
        result = self.cur.execute("""SELECT * FROM films
            """).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'film','time']) 
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()