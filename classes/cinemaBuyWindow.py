from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui
from classes import hallsBuyWindow
import sqlite3


class CinemaBuyWindow(QMainWindow):
    def __init__(self, filmsBuyWindow):
        super().__init__()
        uic.loadUi('windows/cinema_buy.ui', self) 
        self.setWindowIcon(QtGui.QIcon("img/icon.png"))
        self.filmsBuyWindow = filmsBuyWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
       
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_4.clicked.connect(self.back)
        self.refresh()
    
    def back(self):
        self.filmsBuyWindow.show()
        self.filmsBuyWindow.refresh()
        self.close()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.filmsBuyWindow.show()
            self.filmsBuyWindow.refresh()
            self.close()


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

    def select(self):
        if 0 < len(self.tableWidget.selectedItems()) <= 1:
            row = self.tableWidget.selectedItems()[0].row()
            self.cinema_id = self.tableWidget.takeItem(row, 0).text()
            self.film_id = self.filmsBuyWindow.film_id
            self.hallsBuy = hallsBuyWindow.HallsBuyWindow(self)
            self.hallsBuy.show()
            self.close()
            

    
    def refresh(self):
        
        # размеры таблицы
        cinemaIds = self.cur.execute("SELECT cinema_id FROM timetable WHERE film_id=?",
                         (self.filmsBuyWindow.film_id, )).fetchall()
        cinemaIds = [i[0] for i in set(cinemaIds)]
        result = self.cur.execute(f"SELECT * FROM cinemas WHERE id IN (" + ", ".join('?' * len(cinemaIds)) + ")", cinemaIds).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'cinema']) 
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()
