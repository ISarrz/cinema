from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtGui
from classes import hallsSettingsWindow
import sqlite3


class CinemaSettingsWindow(QMainWindow):
    def __init__(self, settingsWindow):
        super().__init__()
        uic.loadUi('windows/sinema_settings.ui', self) 
        self.setWindowIcon(QtGui.QIcon("img/icon.png"))
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
        self.close()

    def keyPressEvent(self, event):
         if event.key() == Qt.Key_Escape:
            self.settingsWindow.show()
            self.close()

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
            rows = [i.row() for i in self.tableWidget.selectedItems()]
            ids = [self.tableWidget.takeItem(row, 1).text() for row in rows]
            self.cur.execute(f"DELETE FROM cinemas WHERE id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
            self.cur.execute(f"DELETE FROM halls WHERE cinema_id IN (" + ", ".join(
            '?' * len(ids)) + ")", ids)
            self.cur.execute(f"DELETE FROM seats WHERE cinema_id IN (" + ", ".join(
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
        result = self.cur.execute("""SELECT * FROM cinemas
            """).fetchall()
        # размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['id','cinema']) 
        # вывод в таблицу
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.con.commit()
