from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDateTimeEdit
from PyQt5.QtCore import Qt
from PyQt5 import uic
from classes import hallsSettingsWindow
import sqlite3


class FilmsSettingsWindow(QMainWindow):
    def __init__(self, settingsWindow):
        super().__init__()
        uic.loadUi('windows/films_settings.ui', self) 
        self.settingsWindow = settingsWindow
        self.con = sqlite3.connect("cinema.db")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.delete)
        self.pushButton_5.clicked.connect(self.find)
        self.pushButton_3.clicked.connect(self.save)
        self.pushButton_4.clicked.connect(self.back)
        self.modified = []
        self.titles = None
        self.rf = False
        self.refresh()
        self.tableWidget.itemChanged.connect(self.item_changed)
        
        

    def item_changed(self, item):
        row = item.row()
        col = item.column()
        if col == 0:
            return
        elif col == 1:
            msg = 'film'
        else:
            msg = 'time'
        if not self.rf:
            id = self.tableWidget.takeItem(row, 0).text()
            self.modified = [id, [msg, item.text()]]
        pass



    def back(self):
        self.settingsWindow.show()
        self.close()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.settingsWindow.show()
            self.close()

    def add(self):
        self.cur.execute(f"""INSERT INTO films(film, time) VALUES('{self.lineEdit.text()}', '{self.timeEdit.time().toString()}')""").fetchall()
        self.refresh()


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

    def delete(self):
        if 0 < len(self.tableWidget.selectedItems()):
            # удаление выделенных id 
            rows = [i.row() for i in self.tableWidget.selectedItems()]
            ids = [self.tableWidget.takeItem(row, 1).text() for row in rows]
            self.cur.execute(f"DELETE FROM films WHERE id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
            self.cur.execute(f"DELETE FROM timetableSeats WHERE film_id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
            self.cur.execute(f"DELETE FROM timetable WHERE film_id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
        # обновление таблицы
        self.refresh()


          
    def save(self):
        if self.modified:
            cur = self.con.cursor()
            b = self.modified
            cur.execute(f"UPDATE films SET {b[1][0]}='{b[1][1]}' WHERE id={b[0]}")
            self.con.commit()
            self.modified.clear()
        self.refresh()

    
    def refresh(self):
        self.rf = True
        result = self.cur.execute("""SELECT * FROM films
            """).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['id','film','time']) 
        self.titles = [description[0] for description in self.cur.description]
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()
        self.modified = {}
        self.rf = False