#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import sys
import os
import api
import think
from time import sleep


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
	game = dict()
	grid = dict()
	grid['x'] = (-28, 28)
	grid['y'] = (-20, 20)
	u_token = "54983a0e-ad70-42d8-bf1a-18341175057e"
	u_id = "af05f814-a669-4287-8ffb-a317d831a4f6"
	conn = sqlite_connect(get_script_path() + "/centralDB.db")

	g_data = api.init_game(conn, u_token, sys.argv)
	g_id = g_data[0]
	g_token = g_data[1]
	if len(sys.argv) > 1:
		game = api.regenerate_db(u_token, g_token, grid)
		sleep(1)

	opp_id = api.waiting(conn, u_token, g_token, u_id)
	sleep(1)
	while True:
		game = api.last_hit(conn, g_id, g_token, u_token, u_id, game, grid)
		think_return = think.thinking(game, grid, u_id, opp_id)
		game = api.send_hit(conn, g_id, g_token, u_token, u_id, opp_id, think_return, game, grid)


main()
