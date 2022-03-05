#!/usr/bin/python3

from time import sleep
import requests
import json
import think


# {"statusCode":226,"playerCrossId":"30fc486c-0d9a-48de-a7fb-b175fe19530f","playerCircleId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","actualPlayerId":"30fc486c-0d9a-48de-a7fb-b175fe19530f","winnerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","coordinates":[{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":3,"y":-7}],"headers":{}}
# {"statusCode":201,"gameToken":"a103d003-e081-4d3a-8848-2295b484efef","gameId":"908be60f-0697-47e1-ad3b-bff5e6e09194","headers":{}}
# {"statusCode":200,"playerCrossId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","playerCircleId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","actualPlayerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","winnerId":null,"coordinates":[{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-1,"y":-3}],"headers":{}}
# {"statusCode":200,"playerCrossId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","playerCircleId":null,"actualPlayerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","winnerId":null,"coordinates":[],"headers":{}}
# {"statusCode":200,"playerCrossId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","playerCircleId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","actualPlayerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","winnerId":null,"coordinates":[{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":1,"y":-5},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":0,"y":-4},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-5,"y":-5},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-4,"y":-4},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-2,"y":-3},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-4,"y":-3},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-4,"y":0},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-1,"y":-3},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":0,"y":0},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-2,"y":-2},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-3,"y":-4},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-3,"y":-3},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":0,"y":2},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-3,"y":-2},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-4,"y":-2},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-1,"y":1},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-2,"y":-1},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-3,"y":-1},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-3,"y":1},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-1,"y":-1},{"playerId":"cbf38348-96e1-4617-b679-aa8a7485c5e0","x":-1,"y":0},{"playerId":"81b7fc85-566e-43b2-aa6e-e63ab1d589db","x":-2,"y":0}],"headers":{}}

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
    if len(args) > 1:
        cur = conn.cursor()
        cur.execute("SELECT gToken FROM games WHERE gID = ?;", [args[1]])
        row = cur.fetchone()
        if row:
            return row[0]
        else:
            print("Wrong Game ID... Bye")
            exit()

    res = req("connect", u_token)
    # print(res)  # pak smazat
    if res['statusCode'] < 400:
        g_token = res['gameToken']
        g_id = res['gameId']
        cur = conn.cursor()
        cur.execute("INSERT INTO games ( gID, gToken, status ) VALUES (?, ?, 'waiting')", [g_id, g_token])
        conn.commit()
        print("python3 main.py " + g_id)
        return g_token
    else:
        print("Something is wrong...")
        print(str(res))
        exit()


def last_hit(conn, g_token, u_token, u_id, game, grid):
    i = 0
    while True:
        res = req("checkLastStatus", u_token, g_token)
        # print(res)  # smazat po devu

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
        # print(res)  # smazat po devu

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

    while True:
        try:
            domain = "https://piskvorky.jobs.cz/api/v1/"
            req_res = requests.post(domain + uri, headers=headers, json=json_data).json()
            return req_res
        except requests.ConnectionError:
            sleep(2)


def send_hit(conn, g_token, u_token, u_id, opp_id, next_hit, game, grid):
    print('Send my hit ' + str(next_hit))
    while True:
        res = req("play", u_token, g_token, next_hit)
        # print(res)  # smazat po devu

        if res['statusCode'] < 220:
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
            next_hit = think.thinking(game, grid, u_id, opp_id)


def waiting(conn, u_token, g_token, u_id):
    while True:
        res = req("checkLastStatus", u_token, g_token)
        # print(res)  # smazat po devu

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
