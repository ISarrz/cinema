from PyQt5.QtWidgets import QMainWindow

from PyQt5.QtCore import Qt
from PyQt5.QtGui import * 
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sqlite3
from classes import timetableWindow
class MyWidget(QMainWindow):
    def __init__(self, seats, st):
        super().__init__()
        self.book = []
        self.select = None
        self.timetableBuyWindow = st.timetableBuyWindow
        self.cinema_id = st.cinema_id
        self.hall_id = st.hall_id
        self.timetable_id = st.timetable_id
        self.con = st.con
        self.cur = st.cur
        self.st = st
        self.timeTableWindow = timetableWindow.TimetableSettingsWindow(self)
        if seats:
            spis = [[i[4], i[5], i[9]] for i in seats]
            self.col = max(spis, key=lambda x: x[1])[1] + 1
            self.row = max(spis, key=lambda x: x[0])[0] + 1
            self.matrix = [[''] * self.col for _ in range(self.row)]
        else:
            self.matrix = []
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        if self.matrix:

            Dialog.resize(len(self.matrix[0])  * 20 + 300, len(self.matrix)  * 20 + 200)
            self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
            self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 100, len(self.matrix[0])  * 20 + 200,  len(self.matrix)  * 20 + 100))
            self.gridLayoutWidget.setObjectName("gridLayoutWidget")
            self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.gridLayout.setObjectName("gridLayout")
            for i in range(len(self.matrix)):
                for g in range(len(self.matrix[0])):

                    seat = self.cur.execute("SELECT free FROM timetableSeats WHERE hall_id=? and cinema_id=? and timetable_id = ? and row = ? and col=?",
                         (self.st.hall_id, self.st.cinema_id, self.timetable_id, i, g)).fetchall()

                    if seat:
                        seat = seat[0][0]

                    
                    if seat == 1:
                        self.book.append(QtWidgets.QPushButton(self.gridLayoutWidget))
                        self.book[-1].setObjectName(f"pushButton_{i}_{g}")
                        self.book[-1].setText(' ')
                        self.book[-1].clicked.connect(self.selected)
                        self.gridLayout.addWidget(self.book[-1], i, g, 1, 1)
                    elif seat == 0:
                        self.book.append(QtWidgets.QPushButton(self.gridLayoutWidget))
                        self.book[-1].setObjectName(f"pushButton_{i}_{g}")
                        self.book[-1].setText('X')
                        self.gridLayout.addWidget(self.book[-1], i, g, 1, 1)
        else:
            Dialog.resize(200, 100)

        self.btnf = QtWidgets.QPushButton(Dialog)
        self.btnf.setGeometry(QtCore.QRect(200,40,100,20 ))
        self.btnf.setObjectName("btnf")
        self.btnf.setText('Купить')
        self.btnf.clicked.connect(self.buy)
        Dialog.setObjectName("Widget Art")
    def selected(self):
        row, col = self.sender().objectName().split('_')[1:]
        self.select = self.cur.execute(f"SELECT id FROM timeTableSeats WHERE row = {row} and col = {col} and hall_id={self.hall_id} and cinema_id={self.cinema_id} and timetable_id={self.timetable_id}").fetchall()
        if self.select:
            self.select = self.select[0][0]
    def buy(self):
        if self.select:
            self.cur.execute(f"UPDATE timetableSeats SET free = False WHERE id={self.select}").fetchall()
            self.refresh()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.timetableBuyWindow.show()
            self.timetableBuyWindow.refresh()
            self.close()

    
    
        
    def refresh(self):
        seats = self.cur.execute("SELECT * FROM timeTableSeats WHERE hall_id=? and cinema_id=? and timetable_id=?",
                         (self.st.hall_id, self.st.cinema_id, self.timetable_id)).fetchall()
        if seats:
            spis = [[i[4], i[5], i[9]] for i in seats]
            self.col = max(spis, key=lambda x: x[1])[1] + 1
            self.row = max(spis, key=lambda x: x[0])[0] + 1
            self.matrix = [[''] * self.col for _ in range(self.row)]
        else:
            self.matrix = []
        self.setupUi(self)
        self.st.ex.close()
        self.ex = MyWidget(seats, self)
        self.ex.show()
        self.con.commit()


class SeatsBuyWindow(QMainWindow):
    def __init__(self, timetableBuyWindow):
        super().__init__()
        self.timetableBuyWindow = timetableBuyWindow
        self.hall_id, self.cinema_id, self.timetable_id = timetableBuyWindow.hall_id, timetableBuyWindow.cinema_id, timetableBuyWindow.timetable_id
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.seats = self.cur.execute("SELECT * FROM timetableSeats WHERE hall_id=? and cinema_id=? and timetable_id=?",
                         (self.hall_id, self.cinema_id, self.timetable_id)).fetchall()

        self.ex = MyWidget(self.seats, self)
        self.ex.show()
       

        pass