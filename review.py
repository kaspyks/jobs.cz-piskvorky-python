#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from time import sleep
import sqlite3
from sqlite3 import Error
import sys
import os
import api


def get_g_token(conn, g_id):
    cur = conn.cursor()
    cur.execute("SELECT gToken FROM games WHERE gID = ?;", [g_id])
    row = cur.fetchone()
    if row:
        return row[0]
    else:
        print("Wrong Game ID... Bye")
        exit()


def get_data(u_token, g_token):
    while True:
        res = api.req("checkStatus", u_token, g_token)
        # print(res)  # smazat po devu

        if res['statusCode'] < 400:
            return res
        elif res['statusCode'] == 429:
            sleep(3)
        else:
            sleep(1)


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def set_column(grid, grid_layout, w, label, x, y, val):
    grid_layout.removeWidget(label[x][y])
    label[x][y].deleteLater()
    label[x][y].widget_name = None
    label[x][y] = QLabel(str(val), w)
    label[x][y].setStyleSheet("border-top: 1px solid black;border-right: 1px solid black;")
    grid_layout.addWidget(label[x][y], 1 + abs(grid['y'][0]) - x, y + abs(grid['x'][0]))

def sqlite_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


def main():
    grid = dict()
    grid['x'] = (-28, 28)
    grid['y'] = (-19, 20)
    u_token = "54983a0e-ad70-42d8-bf1a-18341175057e"
    u_id = "af05f814-a669-4287-8ffb-a317d831a4f6"
    conn = sqlite_connect(get_script_path() + "/centralDB.db")
    g_token = get_g_token(conn, str(sys.argv[1]))
    data_list = get_data(u_token, g_token)
    actual_position = last_position = len(data_list)

    app = QApplication(sys.argv)

    w = QWidget()
    grid_layout = QGridLayout()
    grid_layout.setSpacing(0)
    w.setLayout(grid_layout)
    w.move(300, 300)
    label = dict()
    for i in range(abs(grid['y'][0]) + grid['y'][1] + 1):
        i_real = grid['y'][1] - i
        label[i_real] = dict()
        for j in range(abs(grid['x'][0]) + grid['x'][1] + 1):
            j_real = j + grid['x'][0]
            label[i_real][j_real] = QLabel("   ", w)
            if i == (abs(grid['y'][0]) + grid['y'][1]) and j == 0:
                label[i_real][j_real].setStyleSheet("border-bottom: 1px solid black; border-right: 1px solid black; \
                                    border-top: 1px solid black; border-left: 1px solid black;")
            elif i == (abs(grid['y'][0]) + grid['y'][1]) and j != 0:
                label[i_real][j_real].setStyleSheet("border-top: 1px solid black; border-right: 1px solid black; \
                                    border-bottom: 1px solid black;")
            elif i != (abs(grid['y'][0]) + grid['y'][1]) and j == 0:
                label[i_real][j_real].setStyleSheet("border-top: 1px solid black; border-right: 1px solid black; \
                                    border-left: 1px solid black;")
            else:
                label[i_real][j_real].setStyleSheet("border-top: 1px solid black;border-right: 1px solid black;")
            grid_layout.addWidget(label[i_real][j_real], i, j)


    for data in data_list['coordinates']:
        x = data['y']
        y = data['x']
        if data['playerId'] == data_list['playerCircleId']:
            val = 0
        else:
            val = 1
        set_column(grid, grid_layout, w, label, x, y, val)

    w.setWindowTitle('Piskvorky review')
    w.show()
    sys.exit(app.exec_())
main()
