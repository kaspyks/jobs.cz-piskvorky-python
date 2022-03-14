#!/usr/bin/env python3

from time import sleep
import requests
import json
import think


def completed_game(conn, res, g_token, u_id):
    cur = conn.cursor()
    if res['winnerId'] == u_id:
        print("Congrats! You are winner")
        cur.execute("UPDATE games SET status = 'winner' WHERE gToken = ?;", [g_token])
    else:
        print("You are looser")
        cur.execute("UPDATE games SET status = 'looser' WHERE gToken = ?;", [g_token])
    conn.commit()
    exit()


def edit_game_dict(res, game, grid):
    for j in res['coordinates']:
        x = j['x']
        y = j['y']
        player_id = j['playerId']

        if x not in game:
            game[x] = dict()
        game[x][y] = player_id

        for i in {1, 2, 3}:
            if x + 1 <= grid['x'][1]:
                if x + i not in game:
                    game[x + i] = dict()
                if y + i not in game[x + i] and y + i <= grid['y'][1]:
                    game[x + i][y + i] = 1
                if y not in game[x + i]:
                    game[x + i][y] = 1
                if y - i not in game[x + i] and y - i >= grid['y'][0]:
                    game[x + i][y - i] = 1

            if x - 1 >= grid['x'][0]:
                if x - i not in game:
                    game[x - i] = dict()
                if y - i not in game[x - i] and y - i >= grid['y'][0]:
                    game[x - i][y - i] = 1
                if y not in game[x - i]:
                    game[x - i][y] = 1
                if y + i not in game[x - i] and y + i <= grid['y'][1]:
                    game[x - i][y + i] = 1

            if y + i not in game[x] and y + i <= grid['y'][1]:
                game[x][y + i] = 1
            if y - i not in game[x] and y - i >= grid['y'][0]:
                game[x][y - i] = 1

    return game


def init_game(conn, u_token, args):
    print('Init game')
    cur = conn.cursor()
    table_games_exists = cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='games';").fetchall()
    if not table_games_exists:
        cur.execute("CREATE TABLE games (gID VARCHAR (50), gToken VARCHAR (50), status VARCHAR (50), tries INTEGER, \
        UNIQUE (gID, gToken));")
        conn.commit()
    if len(args) > 1:
        cur.execute("SELECT gID, gToken FROM games WHERE gID = ?;", [args[1]])
        row = cur.fetchone()
        if row:
            return [row[0], row[1]]
        else:
            print("Wrong Game ID... Bye")
            exit()

    res = req("connect", u_token)
    if res['statusCode'] < 400:
        g_token = res['gameToken']
        g_id = res['gameId']
        print("python3 main.py " + g_id)
        cur.execute("INSERT INTO games ( gID, gToken, status ) VALUES (?, ?, 'waiting')", [g_id, g_token])
        sql_prepare = "CREATE TABLE `{}` (id INTEGER PRIMARY KEY AUTOINCREMENT, data VARCHAR (5000));".format(g_id)
        cur.execute(sql_prepare)
        conn.commit()
        print("python3 main.py " + g_id)
        return [g_id, g_token]
    else:
        print("Something is wrong...")
        print(str(res))
        exit()


def last_hit(conn, g_id, g_token, u_token, u_id, game, grid):
    i = 0
    while True:
        res = req("checkLastStatus", u_token, g_token)

        if res['statusCode'] < 220:
            if res['actualPlayerId'] != u_id:
                if i > 100:
                    print("Timeouted...")
                    exit()
                print("Last hit - Opponent's turn")
                sleep(3)
                i += 1
                continue
            else:
                if res['coordinates']:
                    print("Opponent hit [" + str(res['coordinates'][0]['x']) + ", "
                          + str(res['coordinates'][0]['y']) + "]")
                    cur = conn.cursor()
                    sql_prepare = "INSERT INTO `{}` ( data ) VALUES (?)".format(g_id)
                    cur.execute(sql_prepare, [str(res)])
                    conn.commit()
                game = edit_game_dict(res, game, grid)
                return game
        elif res['statusCode'] == 226:
            completed_game(conn, res, g_token, u_id)
            return game
        elif res['statusCode'] == 429:
            print(res)
            sleep(3)
            i += 1
        else:
            print(res)
            sleep(1)
            game = regenerate_db(u_token, g_token, grid)


def regenerate_db(u_token, g_token, grid):
    print("Regenerate DB")
    game = dict()
    while True:
        res = req("checkStatus", u_token, g_token)

        if res['statusCode'] < 400:
            game = edit_game_dict(res, game, grid)
            return game
        elif res['statusCode'] == 429:
            print(res)
            sleep(3)
        else:
            print(res)
            sleep(1)


def req(uri, u_token, g_token="", next_hit=""):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    json_data = json.loads('{ "userToken": "' + u_token + '"}')
    if uri == "play" or uri == "checkStatus" or uri == "checkLastStatus":
        json_data.update({"gameToken": g_token})
    if uri == "play":
        json_data.update({"positionX": next_hit[0]})
        json_data.update({"positionY": next_hit[1]})

    domain = "https://piskvorky.jobs.cz/api/v1/"
    while True:
        try:
            req_res = requests.post(domain + uri, headers=headers, json=json_data).json()
            if "statusCode" not in req_res:
                sleep(1)
                continue
            return req_res
        except (requests.exceptions.ConnectionError, json.decoder.JSONDecodeError):
            sleep(2)


def send_hit(conn, g_id, g_token, u_token, u_id, opp_id, think_return, game, grid):
    print('Send my hit ' + str(think_return[0]))
    while True:
        res = req("play", u_token, g_token, think_return[0])

        if res['statusCode'] < 220:
            cur = conn.cursor()
            res['coordinates'][0]['score'] = think_return[1]
            sql_prepare = "INSERT INTO `{}` ( data ) VALUES (?)".format(g_id)
            cur.execute(sql_prepare, [str(res)])
            conn.commit()
            print('Hit sent')
            game = edit_game_dict(res, game, grid)
            return game
        elif res['statusCode'] == 226:
            completed_game(conn, res, g_token, u_id)
            return game
        elif res['statusCode'] == 429:
            print(res)
            sleep(3)
        else:
            print(res)
            sleep(1)
            game = regenerate_db(u_token, g_token, grid)
            think_return = think.thinking(game, grid, u_id, opp_id)


def waiting(conn, u_token, g_token, u_id):
    while True:
        res = req("checkLastStatus", u_token, g_token)

        if res['statusCode'] < 220:
            if not res['playerCircleId'] or not res['playerCrossId']:
                print("Waiting for second player")
                sleep(3)
                continue
            else:
                print("Let's play")
                break
        elif res['statusCode'] == 226:
            completed_game(conn, res, g_token, u_id)
            break
        elif res['statusCode'] == 429:
            print(res)
            sleep(3)
        else:
            print(res)
            sleep(1)
    if res['playerCircleId'] != u_id:
        opp_id = res['playerCircleId']
    else:
        opp_id = res['playerCrossId']
    cur = conn.cursor()
    cur.execute("UPDATE games SET status = ? WHERE gToken = ?;", [opp_id, g_token])
    conn.commit()
    return opp_id
