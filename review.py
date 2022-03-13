#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sqlite3
from sqlite3 import Error
import sys
import os


def get_data(conn, g_id):
    cur = conn.cursor()
    sql_prepare = "SELECT data FROM `{}` ORDER BY id ASC;".format(g_id)
    cur.execute(sql_prepare)
    records = cur.fetchall()
    res = []
    for row in records:
        res.append(eval(row[0]))
    return res


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def sqlite_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


class MainWindow(QWidget):
    def __init__(self, actual_position, last_position, grid, data_list):
        super().__init__()
        self.actual_position = actual_position
        self.last_position = last_position
        self.grid = grid
        self.data_list = data_list
        self.score_info = QLabel(" ", self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.pressed_left()
        if event.key() == Qt.Key_Right:
            self.pressed_right()

    def pressed_left(self):
        if self.actual_position >= 0:
            x = self.data_list[self.actual_position]['coordinates'][0]['y']
            y = self.data_list[self.actual_position]['coordinates'][0]['x']
            self.set_column(x, y, "   ")
            self.actual_position -= 1

    def pressed_right(self):
        tmp_actual_position = self.actual_position + 1
        if tmp_actual_position <= self.last_position:
            x = self.data_list[tmp_actual_position]['coordinates'][0]['y']
            y = self.data_list[tmp_actual_position]['coordinates'][0]['x']
            if self.data_list[tmp_actual_position]['coordinates'][0]['playerId'] == self.data_list[0]['playerCircleId']:
                self.set_column(x, y, 0)
            else:
                self.set_column(x, y, 1)
            self.actual_position = tmp_actual_position

    def set_column(self, x, y, val):
        self.grid_layout.removeWidget(self.label[x][y])
        self.label[x][y].deleteLater()
        self.label[x][y].widget_name = None
        self.label[x][y] = QLabel(str(val), self)
        self.label[x][y].setStyleSheet("border-top: 1px solid black;border-right: 1px solid black;")
        self.grid_layout.addWidget(self.label[x][y], abs(self.grid['y'][0]) - x, y + abs(self.grid['x'][0]))

        self.grid_layout.removeWidget(self.score_info)
        self.score_info.deleteLater()
        self.score_info.widget_name = None
        if "score" in self.data_list[self.actual_position - 1]['coordinates'][0]:
            self.score_info = QLabel("Score: " + str(
                self.data_list[self.actual_position - 1]['coordinates'][0]['score']), self)
        else:
            self.score_info = QLabel("Opponent's hit", self)
        self.grid_layout.addWidget(self.score_info, abs(self.grid['y'][0]) + self.grid['y'][1] + 1, 0, 1, 10)

        self.show()


def main():
    grid = dict()
    grid['x'] = (-28, 28)
    grid['y'] = (-20, 20)
    u_id = "af05f814-a669-4287-8ffb-a317d831a4f6"
    conn = sqlite_connect(get_script_path() + "/centralDB.db")
    data_list = get_data(conn, str(sys.argv[1]))
    actual_position = last_position = len(data_list) - 1

    app = QApplication([])
    app.setStyleSheet('.QLabel { font-family: sans-serif;}')
    w = MainWindow(actual_position, last_position, grid, data_list)
    w.grid_layout = QGridLayout()
    w.grid_layout.setSpacing(0)
    w.setLayout(w.grid_layout)
    w.move(300, 300)

    w.label = dict()
    for i in range(abs(grid['y'][0]) + grid['y'][1] + 1):
        i_real = grid['y'][1] - i
        w.label[i_real] = dict()
        for j in range(abs(grid['x'][0]) + grid['x'][1] + 1):
            j_real = j + grid['x'][0]
            w.label[i_real][j_real] = QLabel("   ", w)
            
            if i == (abs(grid['y'][0]) + grid['y'][1]) and j == 0:
                w.label[i_real][j_real].setStyleSheet("border-bottom: 1px solid black; border-right: 1px solid black; \
                                    border-top: 1px solid black; border-left: 1px solid black;")
            elif i == (abs(grid['y'][0]) + grid['y'][1]) and j != 0:
                w.label[i_real][j_real].setStyleSheet("border-top: 1px solid black; border-right: 1px solid black; \
                                    border-bottom: 1px solid black;")
            elif i != (abs(grid['y'][0]) + grid['y'][1]) and j == 0:
                w.label[i_real][j_real].setStyleSheet("border-top: 1px solid black; border-right: 1px solid black; \
                                    border-left: 1px solid black;")
            else:
                w.label[i_real][j_real].setStyleSheet("border-top: 1px solid black;border-right: 1px solid black;")
            w.grid_layout.addWidget(w.label[i_real][j_real], i, j)

    w.score_info = QLabel(" ", w)
    w.grid_layout.addWidget(w.score_info, abs(w.grid['y'][0]) + w.grid['y'][1] + 1, 0, 1, 10)

    for data in data_list:
        x = data['coordinates'][0]['y']
        y = data['coordinates'][0]['x']
        if data['coordinates'][0]['playerId'] == data['playerCircleId']:
            val = 0
        else:
            val = 1
        w.set_column(x, y, val)

    if data_list[0]['playerCircleId'] == u_id:
        intro_text = "1 - opposite vs. 0 - kaspy_dev"
    else:
        intro_text = "1 - kaspy_dev vs. 0 - opposite"
    w.setWindowTitle("Piskvorky review " + intro_text)
    w.show()
    sys.exit(app.exec_())


main()
