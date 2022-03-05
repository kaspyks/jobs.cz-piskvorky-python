#!/usr/bin/python3

import sqlite3
from sqlite3 import Error
import sys
import os
import api
import think


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
	grid['y'] = (-19, 20)
	u_token = "54983a0e-ad70-42d8-bf1a-18341175057e"
	u_id = "af05f814-a669-4287-8ffb-a317d831a4f6"
	conn = sqlite_connect(get_script_path() + "/centralDB.db")

	g_token = api.init_game(conn, u_token, sys.argv)
	if len(sys.argv) > 1:
		game = api.regenerate_db(u_token, g_token, grid)

	opp_id = api.waiting(conn, u_token, g_token, u_id)
	while True:
		game = api.last_hit(conn, g_token, u_token, u_id, game, grid)
		next_hit = think.thinking(game, grid, u_id, opp_id)
		game = api.send_hit(conn, g_token, u_token, u_id, opp_id, next_hit, game, grid)


main()
