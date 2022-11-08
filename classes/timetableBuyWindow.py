from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import seatsBuyWindow
import sqlite3


class TimetableBuyWindow(QMainWindow):
    def __init__(self, hallsBuyWindow):
        super().__init__()
        uic.loadUi('windows/cinema_buy.ui', self) 
        self.hallsBuyWindow = hallsBuyWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.film_id, self.cinema_id, self.hall_id = hallsBuyWindow.film_id, hallsBuyWindow.cinema_id, hallsBuyWindow.hall_id
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_4.clicked.connect(self.back)
        self.refresh()
    
    def back(self):
        self.hallsBuyWindow.show()
        self.hallsBuyWindow.refresh()
        self.close()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.hallsBuyWindow.show()
            self.hallsBuyWindow.refresh()
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
            self.timetable_id = self.tableWidget.takeItem(row, 0).text()
            
            self.seatsBuyWindow = seatsBuyWindow.SeatsBuyWindow(self)
            self.close()
            

    
    def refresh(self):
        
        timetableIds = self.cur.execute("SELECT id FROM timetable WHERE film_id=? and cinema_id=? and hall_id =?",
                         (self.film_id, self.cinema_id, self.hall_id)).fetchall()
        timetableIds = [i[0] for i in set(timetableIds)]
        result = self.cur.execute(f"SELECT * FROM timetable WHERE id IN (" + ", ".join('?' * len(timetableIds)) + ")", timetableIds).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['id', 'start', 'end', 'hall id' , 'film id', 'cinema id']) 
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()