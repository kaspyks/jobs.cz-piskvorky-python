#!/usr/bin/env python3

from tkinter import *
import time
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
            return res['coordinates']
        elif res['statusCode'] == 429:
            sleep(3)
        else:
            sleep(1)


def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


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
    actual_position = len(data_list)

    window = Tk()
    # take the data
    lst = [(1, 'Raj', 'Mumbai', 19),
           (2, 'Aaryan', 'Pune', 18),
           (3, 'Vaishnavi', 'Mumbai', 20),
           (4, 'Rachna', 'Mumbai', 21),
           (5, 'Shubham', 'Delhi', 21)]

    # create root window

    for i in range(grid['y'][1] + abs(grid['y'][0]) + 1):
        for j in range(grid['x'][1] + abs(grid['x'][0]) + 1):
            e = Entry(window, width=3, fg='blue',
                           font=('Arial', 16, 'bold'))
            e.grid(row=i, column=j)
            e.insert(END, str(i) + str(j))

    window.mainloop()
main()
