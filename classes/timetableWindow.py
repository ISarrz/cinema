from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import hallsSettingsWindow
import sqlite3


class TimetableSettingsWindow(QMainWindow):
    def __init__(self, seatsSettingsWindow):
        super().__init__()
        uic.loadUi('windows/timetable_settings.ui', self) 
        self.seatsSettingsWindow = seatsSettingsWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.setWindowTitle('Настройка расписания')
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_6.clicked.connect(self.film_find)
        self.pushButton_3.clicked.connect(self.select)
        self.pushButton_4.clicked.connect(self.back)
        self.film_refresh()
        self.refresh()
    
    def back(self):
        self.seatsSettingsWindow.show()
        self.close()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.seatsSettingsWindow.show()
            self.close()

    def add(self):
        time = self.cur.execute("SELECT * FROM films WHERE id=?",(self.lineEdit.text(), )).fetchall()[0][2]
        time = list(map(int, time.split(':')))
        time = time[0] * 60 * 60 + time[1] * 60 + time[2]
        start = self.dateTimeEdit.dateTime().toString('hh:mm:ss.z')   
        end = self.dateTimeEdit.dateTime().addSecs(time).toString('hh:mm:ss.z')  
        film_id = self.lineEdit.text()   
        self.cur.execute(f"INSERT INTO timetable(start, end, hall_id, film_id, cinema_id) VALUES('{start}', '{end}', {self.seatsSettingsWindow.hall_id}, {film_id}, {self.seatsSettingsWindow.cinema_id})""").fetchall()
        
        timetableId = self.cur.execute("SELECT id FROM timetable WHERE start=? and end=? and hall_id=? and film_id=? and cinema_id=?",
                         (start, end, self.seatsSettingsWindow.hall_id, film_id, self.seatsSettingsWindow.cinema_id)).fetchall()
        self.con.commit()
        seats = self.cur.execute("SELECT * FROM seats WHERE cinema_id=? and hall_id=?",
                         (self.seatsSettingsWindow.cinema_id, self.seatsSettingsWindow.hall_id)).fetchall()
        for seat in seats:
            cinema_id, hall_id, seats_id, row, col, active = seat[0],seat[1],seat[2], seat[3],seat[4],seat[5],
            if active:
                self.cur.execute(f"INSERT INTO timetableSeats(cinema_id, hall_id, timetable_id, row, col, film_id, start, end) VALUES(?,?,?,?,?,?,?,?)",
                      (cinema_id, hall_id, timetableId[0][0], row, col, film_id, start, end)).fetchall()  
        self.refresh()


    def find(self):
        # при пустой строке показывется весь список
        if self.lineEdit.text() == '':
            self.refresh()
            return
        # находим значения по названию кинотеатра
        result = self.cur.execute("SELECT * FROM timetable WHERE film_id=?",
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
            rows = [i.row() for i in self.tableWidget.selectedItems()]
            ids = [self.tableWidget.takeItem(row, 0).text() for row in rows]
            self.cur.execute(f"DELETE FROM timetable WHERE id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
            self.cur.execute(f"DELETE FROM timetableSeats WHERE timetable_id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
           
        # обновление таблицы
        self.refresh()


    def select(self):
        
        if 0 < len(self.tableWidget.selectedItems()) <= 1:
            row = self.tableWidget.selectedItems()[0].row()
            cinema_id = self.tableWidget.takeItem(row, 0).text()
            
            self.hallsSettingsWindow = hallsSettingsWindow.HallsSettingsWindow(cinema_id,self)
            self.hallsSettingsWindow.show()
            self.close()
            

    def refresh(self):
        result = self.cur.execute(f"""SELECT * FROM timetable WHERE hall_id={self.seatsSettingsWindow.hall_id} and cinema_id={self.seatsSettingsWindow.cinema_id} 
            """).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['id','start','end', 'hall id', 'film id', 'cinema id']) 
        self.titles = [description[0] for description in self.cur.description]
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()



    def film_find(self):
        # при пустой строке показывется весь список
        if self.lineEdit_2.text() == '':
            self.film_refresh()
            return
        # находим значения по названию кинотеатра
    
        result = self.cur.execute("SELECT * FROM films WHERE film=?",
                         (self.lineEdit_2.text(), )).fetchall()
        # размеры таблицы
        self.tableWidget_2.setRowCount(len(result))
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(['id','film','time']) 
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))
     


    
    def film_refresh(self):
        result = self.cur.execute("""SELECT * FROM films
            """).fetchall()
        # размеры таблицы
        self.tableWidget_2.setRowCount(len(result))
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(['id','film','time']) 
        self.titles = [description[0] for description in self.cur.description]
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget_2.setItem(i, j, QTableWidgetItem(str(val)))

