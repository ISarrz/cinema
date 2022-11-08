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
        
        self.hallsSettingsWindow = st.hallsSettingsWindow
        self.cinema_id = st.cinema_id
        self.hall_id = st.hall_id
        self.con = st.con
        self.cur = st.cur
        self.st = st
        self.timeTableWindow = timetableWindow.TimetableSettingsWindow(self)
        if seats:
            spis = [[i[3], i[4], i[5]] for i in seats]
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
                    self.book.append(QtWidgets.QPushButton(self.gridLayoutWidget))
                    self.book[-1].setObjectName(f"pushButton_{i}_{g}")
                    seat = self.cur.execute("SELECT active FROM seats WHERE hall_id=? and cinema_id=? and row = ? and col=?",
                         (self.st.hall_id, self.st.cinema_id, i, g)).fetchall()[0][0]
                    if seat:
                        self.book[-1].setText(' ')
                        self.book[-1].clicked.connect(self.switch)
                    else:
                        self.book[-1].setText('X')
                        self.book[-1].clicked.connect(self.switch)
                    self.gridLayout.addWidget(self.book[-1], i, g, 1, 1)
        else:
            Dialog.resize(200, 100)


        Dialog.setObjectName("Widget Art")
        self.btn1 = QtWidgets.QPushButton(Dialog)
        self.btn1.setGeometry(QtCore.QRect(20,20,20,20 ))
        self.btn1.setObjectName("btn1")
        self.btn1.setText('+u')
        self.btn1.clicked.connect(self.add)
        self.btn2 = QtWidgets.QPushButton(Dialog)
        self.btn2.setGeometry(QtCore.QRect(20,60,20,20 ))
        self.btn2.setObjectName("btn2")
        self.btn2.setText('+d')
        self.btn2.clicked.connect(self.add)
        self.btn3 = QtWidgets.QPushButton(Dialog)
        self.btn3.setGeometry(QtCore.QRect(0,40,20,20 ))
        self.btn3.setObjectName("btn3")
        self.btn3.setText('+l')
        self.btn3.clicked.connect(self.add)
        self.btn4 = QtWidgets.QPushButton(Dialog)
        self.btn4.setGeometry(QtCore.QRect(40,40,20,20 ))
        self.btn4.setObjectName("btn4")
        self.btn4.setText('+r')
        self.btn4.clicked.connect(self.add)
        self.btn5 = QtWidgets.QPushButton(Dialog)
        self.btn5.setGeometry(QtCore.QRect(100,20,20,20 ))
        self.btn5.setObjectName("btn1")
        self.btn5.setText('-u')
        self.btn5.clicked.connect(self.add)
        self.btn6 = QtWidgets.QPushButton(Dialog)
        self.btn6.setGeometry(QtCore.QRect(100,60,20,20 ))
        self.btn6.setObjectName("btn2")
        self.btn6.setText('-d')
        self.btn6.clicked.connect(self.add)
        self.btn7 = QtWidgets.QPushButton(Dialog)
        self.btn7.setGeometry(QtCore.QRect(80,40,20,20 ))
        self.btn7.setObjectName("btn3")
        self.btn7.setText('-l')
        self.btn7.clicked.connect(self.add)
        self.btn8 = QtWidgets.QPushButton(Dialog)
        self.btn8.setGeometry(QtCore.QRect(120,40,20,20 ))
        self.btn8.setObjectName("btn4")
        self.btn8.setText('-r')
        self.btn8.clicked.connect(self.add)
        self.btnf = QtWidgets.QPushButton(Dialog)
        self.btnf.setGeometry(QtCore.QRect(200,40,100,20 ))
        self.btnf.setObjectName("btnf")
        self.btnf.setText('Расписание')
        self.btnf.clicked.connect(self.timeTable)
    def timeTable(self):
        self.timeTableWindow.show()
        self.close()

    def switch(self):
        if self.sender().text() == ' ':
            self.sender().setText('X')
            row, col = self.sender().objectName().split('_')[1:]
            self.cur.execute(f"UPDATE seats SET active = False WHERE row = {row} and col = {col} and hall_id={self.hall_id} and cinema_id={self.cinema_id}").fetchall()
            self.con.commit()
        else:
            self.sender().setText(' ')
            row, col = self.sender().objectName().split('_')[1:]
            self.cur.execute(f"UPDATE seats SET active = True WHERE row = {row} and col = {col} and hall_id={self.hall_id} and cinema_id={self.cinema_id}").fetchall()
            self.con.commit()
        self.refresh()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.hallsSettingsWindow.show()
            self.close()

    def add(self):
        if not self.matrix:
            if '+' not in self.sender().text():
                return
            self.cur.execute(f"""INSERT INTO seats(cinema_id, hall_id, row, col) VALUES('{self.st.cinema_id}', {self.st.hall_id}, 0, 0)""").fetchall()
        else:
            if self.sender().text() == '+r':
                for i in range(self.row):
                    self.cur.execute(f"""INSERT INTO seats(cinema_id, hall_id, row, col) VALUES('{self.st.cinema_id}', {self.st.hall_id}, {i}, {self.col})""").fetchall()
            elif self.sender().text() == '+d':
                for i in range(self.col):
                    self.cur.execute(f"""INSERT INTO seats(cinema_id, hall_id, row, col) VALUES('{self.st.cinema_id}', {self.st.hall_id}, {self.row}, {i})""").fetchall()
            elif self.sender().text() == '+l':
                for i in range(self.row):
                    self.cur.execute(f"""INSERT INTO seats(cinema_id, hall_id, row, col) VALUES('{self.st.cinema_id}', {self.st.hall_id}, {i}, {-1})""").fetchall()

                seats = self.cur.execute("SELECT id FROM seats WHERE hall_id=? and cinema_id=?",
                         (self.st.hall_id, self.st.cinema_id)).fetchall()
                ids = [i[0] for i in seats]
                for id in ids:
                    seatCol = self.cur.execute("SELECT col FROM seats WHERE hall_id=? and cinema_id=? and id=?",
                            (self.st.hall_id, self.st.cinema_id, id)).fetchall()[0][0]
                    self.cur.execute(f"UPDATE seats SET col = {seatCol + 1} WHERE id = {id}").fetchall()
            elif self.sender().text() == '+u':
                for i in range(self.col):
                    self.cur.execute(f"""INSERT INTO seats(cinema_id, hall_id, row, col) VALUES('{self.st.cinema_id}', {self.st.hall_id}, {-1}, {i})""").fetchall()

                seats = self.cur.execute("SELECT id FROM seats WHERE hall_id=? and cinema_id=?",
                         (self.st.hall_id, self.st.cinema_id)).fetchall()
                ids = [i[0] for i in seats]
                for id in ids:
                    seatRow = self.cur.execute("SELECT row FROM seats WHERE hall_id=? and cinema_id=? and id=?",
                            (self.st.hall_id, self.st.cinema_id, id)).fetchall()[0][0]
                    self.cur.execute(f"UPDATE seats SET row = {seatRow + 1} WHERE id = {id}").fetchall()
            elif self.sender().text() == '-r':
                self.cur.execute(f"DELETE FROM seats WHERE col={self.col - 1} and hall_id={self.hall_id} and cinema_id={self.cinema_id}")
            elif self.sender().text() == '-d':
                self.cur.execute(f"DELETE FROM seats WHERE row={self.row - 1} and hall_id={self.hall_id} and cinema_id={self.cinema_id}")
            elif self.sender().text() == '-l':
                seats = self.cur.execute("SELECT id FROM seats WHERE hall_id=? and cinema_id=?",
                         (self.st.hall_id, self.st.cinema_id)).fetchall()
                ids = [i[0] for i in seats]
                for id in ids:
                    seatCol = self.cur.execute("SELECT col FROM seats WHERE hall_id=? and cinema_id=? and id=?",
                            (self.st.hall_id, self.st.cinema_id, id)).fetchall()[0][0]
                    if seatCol == 0:
                        self.cur.execute(f"DELETE FROM seats WHERE id={id}")
                    else:
                        self.cur.execute(f"UPDATE seats SET col = {seatCol - 1} WHERE id = {id}").fetchall()
            elif self.sender().text() == '-u':
                seats = self.cur.execute("SELECT id FROM seats WHERE hall_id=? and cinema_id=?",
                         (self.st.hall_id, self.st.cinema_id)).fetchall()
                ids = [i[0] for i in seats]
                for id in ids:
                    seatRow = self.cur.execute("SELECT row FROM seats WHERE hall_id=? and cinema_id=? and id=?",
                            (self.st.hall_id, self.st.cinema_id, id)).fetchall()[0][0]
                    if seatRow == 0:
                        self.cur.execute(f"DELETE FROM seats WHERE id={id}")
                    else:
                        self.cur.execute(f"UPDATE seats SET row = {seatRow - 1} WHERE id = {id}").fetchall()
        self.refresh()
    
    
        
    def refresh(self):
        seats = self.cur.execute("SELECT * FROM seats WHERE hall_id=? and cinema_id=?",
                         (self.st.hall_id, self.st.cinema_id)).fetchall()
        if seats:
            spis = [[i[3], i[4], i[5]] for i in seats]
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


class SeatsSettingsWindow(QMainWindow):
    def __init__(self, cinema_id, hall_id, hallsSettingsWindow):
        super().__init__()
        self.hallsSettingsWindow = hallsSettingsWindow
        self.cinema_id, self.hall_id = cinema_id, hall_id
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.seats = self.cur.execute("SELECT * FROM seats WHERE hall_id=? and cinema_id=?",
                         (self.hall_id, self.cinema_id)).fetchall()

        self.ex = MyWidget(self.seats, self)
        self.ex.show()
       

        pass





