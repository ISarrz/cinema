from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import timetableBuyWindow
import sqlite3


class HallsBuyWindow(QMainWindow):
    def __init__(self, filmsBuyWindow):
        super().__init__()
        uic.loadUi('windows/halls_buy.ui', self) 
        self.filmsBuyWindow = filmsBuyWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.film_id, self.cinema_id = self.filmsBuyWindow.film_id, self.filmsBuyWindow.cinema_id
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
            self.hall_id = self.tableWidget.takeItem(row, 1).text()
            self.seatsBuyWindow = timetableBuyWindow.TimetableBuyWindow(self)
            self.seatsBuyWindow.show()
            self.close()
            

    
    def refresh(self):
        
        # размеры таблицы
        hallsIds = self.cur.execute("SELECT hall_id FROM timetable WHERE film_id=? and cinema_id = ?",
                         (self.filmsBuyWindow.film_id, self.filmsBuyWindow.cinema_id)).fetchall()
        hallsIds = [i[0] for i in set(hallsIds)]
        result = self.cur.execute(f"SELECT * FROM halls WHERE id IN (" + ", ".join('?' * len(hallsIds)) + ")", hallsIds).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['cinema id','id', 'hal']) 
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()