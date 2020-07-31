#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTableWidgetItem
import pymysql
from pymysql.cursors import DictCursor
import design
import unittest


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        self.__connection = pymysql.connect(
            host='localhost',
            user='root',
            password='FhJ2mn3dweqgE##',
            db='library',
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.table.setColumnCount(3)  # Устанавливаем три колонки
        self.label.setText("")
        self.table.setHorizontalHeaderLabels(["id", "Имя", "Номер"])
        self.reading_text()
        self.lineEdit_2.textChanged.connect(self.search)

        self.pushButton.clicked.connect(self.on_click)
        self.checkBox.clicked.connect(self.reading_text_b)
        self.checkBox_2.clicked.connect(self.creature_text_b)
        self.checkBox_3.clicked.connect(self.update_text_b)
        self.checkBox_4.clicked.connect(self.delete_text_b)
        self.checkBox_5.clicked.connect(self.search_b)

    @pyqtSlot()
    def on_click(self):

        if self.checkBox.isChecked():
            self.reading_text()
        if self.checkBox_2.isChecked():
            self.creature_text()
            self.cleare()
        if self.checkBox_3.isChecked():
            self.update_text()
            self.cleare()
        if self.checkBox_4.isChecked():
            self.delete_text()
            self.cleare()

    def reading_text_b(self):
        self.lineEdit_2.hide()
        self.lineEdit.hide()
        self.pushButton.show()
        self.label.setText("")
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

    def reading_text(self):

        self.table.clear()
        self.table.setRowCount(1)
        with self.__connection.cursor() as cursor:
            sql = "SELECT * FROM `library`.`library`"
            cursor.execute(sql)
            for row in cursor:
                print(row)
                self.table.setItem(self.table.rowCount() -1 , 0, QTableWidgetItem(str(row['id'])))
                self.table.setItem(self.table.rowCount() -1 , 1, QTableWidgetItem(row['name']))
                self.table.setItem(self.table.rowCount() -1 , 2, QTableWidgetItem(str(row['number'])))
                self.table.setRowCount(self.table.rowCount() + 1)  # и одну строку в таблице
        self.table.resizeColumnsToContents()
        print(self.table.rowCount())

    def creature_text_b(self):
        self.lineEdit_2.hide()
        self.lineEdit.show()
        self.pushButton.show()
        self.label.setText("Формат ввод: Имя Номер")
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(True)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
    @pyqtSlot()
    def creature_text(self):

        text = self.lineEdit.text().split(" ")
        with self.__connection.cursor() as cursor:
            sql = f"INSERT INTO library.library (name, number) values ('{text[0]}', '{text[1]}');"
            cursor.execute(sql)
            self.__connection.commit()

    def update_text_b(self):
        self.lineEdit_2.hide()
        self.lineEdit.show()
        self.pushButton.show()
        self.label.setText("Формат ввод:  id Имя Номер")
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(True)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
    def update_text(self):

        text = self.lineEdit.text().split(" ")
        with self.__connection.cursor() as cursor:
            sql = f"UPDATE library.library SET name= '{text[1]}',number='{text[2]}' WHERE id={text[0]}"
            cursor.execute(sql)
            self.__connection.commit()

    def delete_text_b(self):
        self.lineEdit_2.hide()
        self.lineEdit.show()
        self.pushButton.show()
        self.label.setText("Формат ввод: id")
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(True)
        self.checkBox_5.setChecked(False)
    def delete_text(self):

        text = self.lineEdit.text()
        with self.__connection.cursor() as cursor:
            sql = f"DELETE FROM `library`.`library` WHERE id={text}"
            cursor.execute(sql)
            self.__connection.commit()

    def search_b(self):
        self.lineEdit_2.show()
        self.table.clear()
        self.table.setRowCount(1)
        self.label.setText("")
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(True)
        self.lineEdit.hide()
        self.pushButton.hide()

    def search(self):
        self.table.clear()
        self.table.setRowCount(1)
        text = self.lineEdit_2.text()
        with self.__connection.cursor() as cursor:
            sql = f"SELECT * FROM `library`.`library` WHERE concat(name,number) LIKE '%{text}%'"
            cursor.execute(sql)
            for row in cursor:
                print(row)
                self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(row['id'])))
                self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(row['name']))
                self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(str(row['number'])))
                self.table.setRowCount(self.table.rowCount() + 1)  # и одну строку в таблице
            self.table.resizeColumnsToContents()

    def cleare(self):
        self.lineEdit.clear()
        self.reading_text()
        self.reading_text_b()


def main():

    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

