#!/usr/bin/env python3

import random


class Thinking:
    def __init__(self, grid, g_data, u_id, u_token, opp_id):
        self.grid = grid
        self.g_id = g_data[0]
        self.g_token = g_data[1]
        self.u_id = u_id
        self.u_token = u_token
        self.opp_id = opp_id
        self.x = 0
        self.y = 0
        self.actual = ""
        self.opponent = ""
        self.dir_score = 0
        self.ssc = dict()
        self.multiple = 0
        self.special_score = 800
        self.move_no = 0

    def check_square(self, game):
        max_position = 4
        score = 0
        hardening = 0
        for direction in (0, 1, 2, 3):
            # d = direction
            a_s = dict()  # actual_situation
            self.dir_score = 0
            for position in range(1, max_position + 1):
                for i in (1, -1):
                    a_s[position * i] = self.square_state(game, position * i, direction)
                    if not a_s[position * i]:
                        a_s[position * i] = 1

            # skip row where it's not possible to create 5 in row
            opponent_square_positive = 0
            opponent_square_negative = 0
            free_squares = 1
            for i in range(1, max_position + 1):
                if opponent_square_positive == 0:
                    if a_s[i] == self.opponent:
                        opponent_square_positive = 1
                    else:
                        free_squares += 1
                if opponent_square_negative == 0:
                    if a_s[i * (-1)] == self.opponent:
                        opponent_square_negative = 1
                    else:
                        free_squares += 1
            if free_squares < 5:
                continue

            for i in (-1, 1):
                if a_s[1 * i] == self.actual:
                    if a_s[2 * i] == self.actual:
                        if a_s[3 * i] == self.actual:
                            if a_s[4 * i] == self.actual or a_s[-1 * i] == self.actual:  # no. 1, no. 2
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ",no. 1,no. 2")
                                self.count_dir_score(99999, 40000)
                            if a_s[-1 * i] == 1:
                                if a_s[4 * i] == 1:  # no. 4
                                    # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 4")
                                    self.count_dir_score(8000, 3000)
                                if a_s[4 * i] == self.opponent:  # no. 6
                                    # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 6")
                                    self.count_dir_score(600, 500)
                                    hardening += 1
                        if a_s[-1 * i] == self.actual:
                            if a_s[3 * i] == 1:
                                if a_s[-2 * i] == 1:  # no. 5
                                    # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 5")
                                    self.count_dir_score(8000, 3000)
                                if a_s[-2 * i] == self.opponent:  # no. 7
                                    # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 7")
                                    self.count_dir_score(600, 500)
                                    hardening += 1
                            if a_s[-2 * i] == 1 and a_s[3 * i] == self.opponent:  # no. 8
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 8")
                                self.count_dir_score(600, 500)
                                hardening += 1
                        if a_s[3 * i] == 1:
                            if a_s[4 * i] == self.actual:  # no. 30
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 30")
                                self.count_dir_score(580, 470)
                            if a_s[-1 * i] == 1:  # no. 9
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 9")
                                self.count_dir_score(600, 500)
                                hardening += 1
                            if a_s[-1 * i] == self.opponent:  # no. 14
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 14")
                                self.count_dir_score(100, 60)
                        if a_s[3 * i] == self.opponent and a_s[-1 * i] == 1:  # no. 16
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 16")
                            self.count_dir_score(100, 60)
                        if a_s[-1 * i] == 1 and a_s[-2 * i] == self.actual:  # no. 27
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 27")
                            self.count_dir_score(600, 500)
                    if a_s[2 * i] == 1:
                        if a_s[-1 * i] == 1:  # no. 23
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 23")
                            self.count_dir_score(15, 10)
                            if a_s[-2 * i] == self.actual and a_s[-3 * i] == 1:  # no. 13
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 13")
                                self.count_dir_score(550, 450)
                                hardening += 1
                            if a_s[3 * i] == self.actual and a_s[4 * i] == self.opponent:  # no. 20
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 20")
                                self.count_dir_score(100, 60)
                        if a_s[-1 * i] == self.opponent:  # no. 24
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 24")
                            self.count_dir_score(2, 1)
                            if a_s[3 * i] == self.actual and a_s[4 * i] == 1:  # no. 19
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 19")
                                self.count_dir_score(100, 60)
                        if a_s[3 * i] == self.actual:
                            if a_s[-1 * i] == 1 and a_s[4 * i] == 1:  # no. 12
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 12")
                                self.count_dir_score(550, 450)
                                hardening += 1
                            if a_s[-1 * i] == self.actual:  # no. 26
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 26")
                                self.count_dir_score(600, 500)
                        if a_s[-1 * i] == self.actual and a_s[-2 * i] == self.opponent:  # no. 15
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 15")
                            self.count_dir_score(100, 60)
                    if a_s[2 * i] == self.opponent and a_s[-1 * i] == 1:  # no. 25
                        # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 25")
                        self.count_dir_score(2, 1)
                if a_s[1 * i] == 1 and a_s[2 * i] == self.actual:
                    if a_s[3 * i] == self.actual:
                        if a_s[4 * i] == 1:
                            if a_s[-1 * i] == 1:  # no. 11
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 11")
                                self.count_dir_score(550, 450)
                                hardening += 1
                            if a_s[-1 * i] == self.opponent:  # no. 17
                                # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 17")
                                self.count_dir_score(100, 60)
                        if a_s[4 * i] == self.actual:  # no. 29
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 29")
                            self.count_dir_score(580, 470)
                        if a_s[4 * i] == self.opponent and a_s[-1 * i] == 1:  # no. 18
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 18")
                            self.count_dir_score(100, 60)
                        if a_s[-1 * i] == self.actual:  # no. 28
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 28")
                            self.count_dir_score(600, 500)
                    if a_s[-1 * i] == self.actual:
                        if a_s[3 * i] == self.opponent and a_s[-2 * i] == 1:  # no. 21
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 21")
                            self.count_dir_score(100, 60)
                        if a_s[3 * i] == 1 and a_s[-2 * i] == self.opponent:  # no. 22
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 22")
                            self.count_dir_score(100, 60)

            if a_s[1] == self.actual and a_s[-1] == self.actual:
                if a_s[2] == self.actual:
                    if a_s[-2] == self.actual:  # no. 3
                        # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 3")
                        self.count_dir_score(99999, 40000)
                if a_s[2] == 1:
                    if a_s[-2] == 1:  # no. 10
                        # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 10")
                        self.count_dir_score(600, 500)
                        hardening += 1
                        if a_s[3] == self.actual and a_s[-3] == self.actual:  # no. 31
                            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", D: " + str(d) + ", no. 31")
                            self.count_dir_score(8000, 3000)

            score += self.dir_score
        if hardening > 1:
            score = score * 2
            # print("X: " + str(self.x) + ", Y: " + str(self.y) + ", Hardening: " + str(hardening))

        self.dir_score = score
        if self.dir_score < self.special_score and self.actual == self.u_id:
            self.ssc = dict()
            for i in range(-6, 7):
                self.ssc[i] = dict()
                for j in range(-6, 7):
                    self.ssc[i][j] = self.square_state_custom(game, i, j)

            for self.multiple in (1, -1):
                if self.ss("b", 1, 0) and self.ss("a", 1, 1) and self.ss("a", 2, 0) and self.ss("a", 1, -1) \
                        and (self.ss("b", -1, 0) or self.ss("b", 3, 0)) \
                        and (self.ss("b", -1, 0) or self.ss("b", 4, 0)) \
                        and (self.ss("b", 3, 0) or self.ss("b", -2, 0)) \
                        and (self.ss("b", 1, 2) or self.ss("b", 1, -2)) \
                        and (self.ss("b", 1, 2) or self.ss("b", 1, -3)) \
                        and (self.ss("b", 1, -2) or self.ss("b", 1, 3)):  # no. 101
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, -1) and self.ss("a", 2, 0) and self.ss("a", 2, -2) and self.ss("a", 0, -2) \
                        and (self.ss("b", -1, 1) or self.ss("b", 3, -3)) \
                        and (self.ss("b", -1, 1) or self.ss("b", 4, -4)) \
                        and (self.ss("b", 3, -3) or self.ss("b", -2, 2)) \
                        and (self.ss("b", 3, 1) or self.ss("b", -1, -3)) \
                        and (self.ss("b", 3, 1) or self.ss("b", -2, -4))\
                        and (self.ss("b", -1, -3) or self.ss("b", 4, 2)):  # no. 102
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, -1) and self.ss("a", 1, -1) and self.ss("a", 0, -2) and self.ss("a", -1, -1) \
                        and (self.ss("b", 0, 1) or self.ss("b", 0, -3)) \
                        and (self.ss("b", 0, 1) or self.ss("b", 0, -4)) \
                        and (self.ss("b", 0, -3) or self.ss("b", 0, 2)) \
                        and (self.ss("b", 2, -1) or self.ss("b", -2, -1)) \
                        and (self.ss("b", 2, -1) or self.ss("b", 3, -1))\
                        and (self.ss("b", -2, -1) or self.ss("b", -3, -1)):  # no. 103
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, -1) and self.ss("a", 0, -2) and self.ss("a", -2, -2) and self.ss("a", -2, 0) \
                        and (self.ss("b", 1, 1) or self.ss("b", -3, -3)) \
                        and (self.ss("b", 1, 1) or self.ss("b", -4, -4)) \
                        and (self.ss("b", -3, -3) or self.ss("b", 2, 2)) \
                        and (self.ss("b", 1, -3) or self.ss("b", -3, 1)) \
                        and (self.ss("b", 1, -3) or self.ss("b", -4, 2))\
                        and (self.ss("b", -3, 1) or self.ss("b", 2, -4)):  # no. 104
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, 0) and self.ss("a", -1, 0) and self.ss("a", 1, 1) and self.ss("a", 1, -1) \
                        and (self.ss("b", -2, 0) or self.ss("b", 2, 0)) \
                        and (self.ss("b", -2, 0) or self.ss("b", 3, 0)) \
                        and (self.ss("b", 2, 0) or self.ss("b", -3, 0)) \
                        and (self.ss("b", 1, 2) or self.ss("b", 1, -2)) \
                        and (self.ss("b", 1, 2) or self.ss("b", 1, -3))\
                        and (self.ss("b", 1, -2) or self.ss("b", 1, 3)):  # no. 105
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, -1) and self.ss("a", -1, 1) and self.ss("a", 2, 0) and self.ss("a", 0, -2) \
                        and (self.ss("b", 2, -2) or self.ss("b", -2, 2)) \
                        and (self.ss("b", 2, -2) or self.ss("b", -3, 3)) \
                        and (self.ss("b", -2, 2) or self.ss("b", 3, -3)) \
                        and (self.ss("b", 3, 1) or self.ss("b", -1, -3)) \
                        and (self.ss("b", 3, 1) or self.ss("b", -2, -4))\
                        and (self.ss("b", -1, -3) or self.ss("b", 4, 2)):  # no. 106
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, -1) and self.ss("a", 0, 1) and self.ss("a", 1, -1) and self.ss("a", -1, -1) \
                        and (self.ss("b", 0, -2) or self.ss("b", 0, 2)) \
                        and (self.ss("b", 0, -2) or self.ss("b", 0, 3)) \
                        and (self.ss("b", 0, 2) or self.ss("b", 0, -3)) \
                        and (self.ss("b", 2, -1) or self.ss("b", -2, -1)) \
                        and (self.ss("b", 2, -1) or self.ss("b", -3, -1))\
                        and (self.ss("b", -2, -1) or self.ss("b", 3, -1)):  # no. 107
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, -1) and self.ss("a", 1, 1) and self.ss("a", 0, -2) and self.ss("a", -2, 0) \
                        and (self.ss("b", -2, -2) or self.ss("b", 2, 2)) \
                        and (self.ss("b", -2, -2) or self.ss("b", 3, 3)) \
                        and (self.ss("b", 2, 2) or self.ss("b", -3, -3)) \
                        and (self.ss("b", 1, -3) or self.ss("b", -3, 1)) \
                        and (self.ss("b", 1, -3) or self.ss("b", -4, 2))\
                        and (self.ss("b", -3, 1) or self.ss("b", 2, -4)):  # no. 108
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 2, 0) and self.ss("a", 1, 0) and self.ss("a", 2, 1) and self.ss("a", 2, -1) \
                        and (self.ss("b", 3, 0) or self.ss("b", -1, 0)) \
                        and (self.ss("b", 3, 0) or self.ss("b", -2, 0)) \
                        and (self.ss("b", -1, 0) or self.ss("b", 4, 0)) \
                        and (self.ss("b", 2, 2) or self.ss("b", 2, -2)) \
                        and (self.ss("b", 2, 2) or self.ss("b", 2, -3)) \
                        and (self.ss("b", 2, -2) or self.ss("b", 3, 3)):  # no. 109
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 2, -2) and self.ss("a", 1, -1) and self.ss("a", 3, -1) and self.ss("a", 1, -3) \
                        and (self.ss("b", 3, 3) or self.ss("b", -1, -1)) \
                        and (self.ss("b", 3, 3) or self.ss("b", -2, -2)) \
                        and (self.ss("b", -1, -1) or self.ss("b", 4, 4)) \
                        and (self.ss("b", 4, 0) or self.ss("b", 0, -4)) \
                        and (self.ss("b", 4, 0) or self.ss("b", -1, -5)) \
                        and (self.ss("b", 0, -4) or self.ss("b", 5, 1)):  # no. 110
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, -2) and self.ss("a", 0, -1) and self.ss("a", 1, -2) and self.ss("a", -1, -2) \
                        and (self.ss("b", 0, -3) or self.ss("b", 0, 1)) \
                        and (self.ss("b", 0, -3) or self.ss("b", 0, 2)) \
                        and (self.ss("b", 0, 1) or self.ss("b", 0, -4)) \
                        and (self.ss("b", 2, -2) or self.ss("b", -2, -2)) \
                        and (self.ss("b", 2, -2) or self.ss("b", -3, -2)) \
                        and (self.ss("b", -2, -2) or self.ss("b", 3, -2)):  # no. 111
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -2, -2) and self.ss("a", -1, -1) and self.ss("a", -1, -3) and self.ss("a", -3, -1) \
                        and (self.ss("b", -3, -3) or self.ss("b", 1, 1)) \
                        and (self.ss("b", -3, -3) or self.ss("b", 2, 2)) \
                        and (self.ss("b", 1, 1) or self.ss("b", -4, -4)) \
                        and (self.ss("b", 0, -4) or self.ss("b", -4, 0)) \
                        and (self.ss("b", 0, -4) or self.ss("b", -5, 1)) \
                        and (self.ss("b", -4, 0) or self.ss("b", 1, -5)):  # no. 112
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, 1) and self.ss("a", 0, 2) and self.ss("a", -1, 1) and self.ss("a", -2, 1) \
                        and (self.ss("b", 0, 3) or self.ss("b", 0, -1)) \
                        and (self.ss("b", 0, 3) or self.ss("b", 0, -2)) \
                        and (self.ss("b", 0, -1) or self.ss("b", 0, 4)) \
                        and (self.ss("b", -3, 1) or self.ss("b", 1, 1)) \
                        and (self.ss("b", -3, 1) or self.ss("b", 2, 1)) \
                        and (self.ss("b", 1, 1) or self.ss("b", -4, 1)):  # no. 113
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, 1) and self.ss("a", 2, 2) and self.ss("a", -1, 3) and self.ss("a", 0, 2) \
                        and (self.ss("b", 3, 3) or self.ss("b", -1, -1)) \
                        and (self.ss("b", 3, 3) or self.ss("b", -2, -2)) \
                        and (self.ss("b", -1, -1) or self.ss("b", 4, 4)) \
                        and (self.ss("b", -2, 4) or self.ss("b", 2, 0)) \
                        and (self.ss("b", -2, 4) or self.ss("b", 3, -1)) \
                        and (self.ss("b", 2, 0) or self.ss("b", -3, 5)):  # no. 114
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, 0) and self.ss("a", 2, 0) and self.ss("a", 1, 1) and self.ss("a", 1, 2) \
                        and (self.ss("b", 3, 0) or self.ss("b", -1, 0)) \
                        and (self.ss("b", 3, 0) or self.ss("b", -2, 0)) \
                        and (self.ss("b", -1, 0) or self.ss("b", 4, 0)) \
                        and (self.ss("b", 1, -1) or self.ss("b", 1, 3)) \
                        and (self.ss("b", 1, -1) or self.ss("b", 1, 4)) \
                        and (self.ss("b", 1, 3) or self.ss("b", 1, -2)):  # no. 115
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, -1) and self.ss("a", 2, -2) and self.ss("a", 2, 0) and self.ss("a", 3, 1) \
                        and (self.ss("b", 3, 3) or self.ss("b", -1, -1)) \
                        and (self.ss("b", 3, 3) or self.ss("b", -2, -2)) \
                        and (self.ss("b", -1, -1) or self.ss("b", 4, 4)) \
                        and (self.ss("b", 0, -2) or self.ss("b", 4, 2)) \
                        and (self.ss("b", 0, -2) or self.ss("b", 5, 3)) \
                        and (self.ss("b", 4, 2) or self.ss("b", -1, -3)):  # no. 116
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, -1) and self.ss("a", 0, -2) and self.ss("a", -1, -1) and self.ss("a", -2, -1) \
                        and (self.ss("b", 0, -3) or self.ss("b", 0, 1)) \
                        and (self.ss("b", 0, -3) or self.ss("b", 0, 2)) \
                        and (self.ss("b", 0, 1) or self.ss("b", 0, -4)) \
                        and (self.ss("b", 1, -1) or self.ss("b", -3, -1)) \
                        and (self.ss("b", 1, -1) or self.ss("b", -4, -1)) \
                        and (self.ss("b", -3, -1) or self.ss("b", 2, -1)):  # no. 117
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, -1) and self.ss("a", -2, -2) and self.ss("a", -2, 0) and self.ss("a", -3, 1) \
                        and (self.ss("b", -3, -3) or self.ss("b", 1, 1)) \
                        and (self.ss("b", -3, -3) or self.ss("b", 2, 2)) \
                        and (self.ss("b", 1, 1) or self.ss("b", -4, -4)) \
                        and (self.ss("b", 0, -2) or self.ss("b", -4, 2)) \
                        and (self.ss("b", 0, -2) or self.ss("b", -5, -3)) \
                        and (self.ss("b", -4, 2) or self.ss("b", 1, -3)):  # no. 118
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, 0) and self.ss("a", -2, 0) and self.ss("a", -1, 1) and self.ss("a", -1, 2) \
                        and (self.ss("b", -3, 0) or self.ss("b", 1, 0)) \
                        and (self.ss("b", -3, 0) or self.ss("b", 2, 0)) \
                        and (self.ss("b", 1, 0) or self.ss("b", -4, 0)) \
                        and (self.ss("b", -1, -1) or self.ss("b", -1, 3)) \
                        and (self.ss("b", -1, -1) or self.ss("b", -1, 4)) \
                        and (self.ss("b", -1, 3) or self.ss("b", -1, -2)):  # no. 119
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, 1) and self.ss("a", -2, 2) and self.ss("a", 0, 2) and self.ss("a", 1, 3) \
                        and (self.ss("b", -3, 3) or self.ss("b", 1, -1)) \
                        and (self.ss("b", -3, 3) or self.ss("b", 2, -2)) \
                        and (self.ss("b", 1, -1) or self.ss("b", -4, 4)) \
                        and (self.ss("b", -2, 0) or self.ss("b", 2, 4)) \
                        and (self.ss("b", -2, 0) or self.ss("b", 3, 5)) \
                        and (self.ss("b", 2, 4) or self.ss("b", -3, -1)):  # no. 120
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[-1 * self.multiple][0] == self.actual \
                        and self.ssc[1 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[1 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-2 * self.multiple][0] == 1 or self.ssc[-2 * self.multiple][0] == self.actual) \
                        and (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][-3 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 121
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[-1 * self.multiple][0] == self.actual \
                        and self.ssc[1 * self.multiple][1 * self.multiple] == self.actual and \
                        self.ssc[1 * self.multiple][2 * self.multiple] == self.actual \
                        and (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-2 * self.multiple][0] == 1 or self.ssc[-2 * self.multiple][0] == self.actual) \
                        and (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][3 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    3 * self.multiple] == self.actual):  # no. 122
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[0][-2 * self.multiple] == self.actual and self.ssc[-1 * self.multiple][
                    -3 * self.multiple] == self.actual \
                        and (self.ssc[2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-2 * self.multiple][-4 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -4 * self.multiple] == self.actual):  # no. 123
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[2 * self.multiple][0] == self.actual and self.ssc[3 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and (self.ssc[2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) \
                        and (self.ssc[4 * self.multiple][2 * self.multiple] == 1 or self.ssc[4 * self.multiple][
                    2 * self.multiple] == self.actual):  # no. 124
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-1 * self.multiple] == 1 or self.ssc[0][-1 * self.multiple] == self.actual) and \
                        self.ssc[0][1 * self.multiple] == self.actual \
                        and self.ssc[-1 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[-2 * self.multiple][-1 * self.multiple] == self.actual \
                        and (self.ssc[0][2 * self.multiple] == 1 or self.ssc[0][2 * self.multiple] == self.actual) \
                        and (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual):  # no. 125
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-1 * self.multiple] == 1 or self.ssc[0][-1 * self.multiple] == self.actual) and \
                        self.ssc[0][1 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[2 * self.multiple][-1 * self.multiple] == self.actual \
                        and (self.ssc[0][2 * self.multiple] == 1 or self.ssc[0][2 * self.multiple] == self.actual) \
                        and (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-1 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual):  # no. 126
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and self.ssc[-2 * self.multiple][0] == self.actual and self.ssc[-3 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and (self.ssc[-2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][2 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[-4 * self.multiple][2 * self.multiple] == 1 or self.ssc[-4 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][
                    -2 * self.multiple] == self.actual):  # no. 127
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and self.ssc[0][-2 * self.multiple] == self.actual and self.ssc[1 * self.multiple][
                    -3 * self.multiple] == self.actual \
                        and (self.ssc[-2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][2 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][-4 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -4 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][0] == 1 or self.ssc[-2 * self.multiple][
                    0] == self.actual):  # no. 128
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) and \
                        self.ssc[1 * self.multiple][0] == self.actual \
                        and self.ssc[2 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[2 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][0] == 1 or self.ssc[-1 * self.multiple][0] == self.actual) \
                        and (self.ssc[3 * self.multiple][0] == 1 or self.ssc[3 * self.multiple][0] == self.actual) \
                        and (self.ssc[2 * self.multiple][1 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][-3 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 129
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) and \
                        self.ssc[1 * self.multiple][0] == self.actual \
                        and self.ssc[2 * self.multiple][1 * self.multiple] == self.actual and \
                        self.ssc[2 * self.multiple][2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][0] == 1 or self.ssc[-1 * self.multiple][0] == self.actual) \
                        and (self.ssc[3 * self.multiple][0] == 1 or self.ssc[3 * self.multiple][0] == self.actual) \
                        and (self.ssc[2 * self.multiple][-1 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][3 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    3 * self.multiple] == self.actual):  # no. 130
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -2 * self.multiple] == self.actual) and self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][-3 * self.multiple] == self.actual and self.ssc[0][
                    -4 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][5 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    5 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-1 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -1 * self.multiple] == self.actual):  # no. 131
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -2 * self.multiple] == self.actual) and self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[3 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[4 * self.multiple][0] == self.actual \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[5 * self.multiple][1 * self.multiple] == 1 or self.ssc[5 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][-3 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 132
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) and \
                        self.ssc[0][-1 * self.multiple] == self.actual \
                        and self.ssc[-1 * self.multiple][-2 * self.multiple] == self.actual and \
                        self.ssc[-2 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[0][-3 * self.multiple] == 1 or self.ssc[0][-3 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][-2 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -2 * self.multiple] == self.actual):  # no. 133
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) and \
                        self.ssc[0][-1 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][-2 * self.multiple] == self.actual and \
                        self.ssc[2 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[0][-3 * self.multiple] == 1 or self.ssc[0][-3 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-2 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -2 * self.multiple] == self.actual):  # no. 134
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -2 * self.multiple] == self.actual) and self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[-3 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[-4 * self.multiple][0] == self.actual \
                        and (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[-5 * self.multiple][1 * self.multiple] == 1 or self.ssc[-5 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 135
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -2 * self.multiple] == self.actual) and self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[-1 * self.multiple][-3 * self.multiple] == self.actual and self.ssc[0][
                    -4 * self.multiple] == self.actual \
                        and (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][-5 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -5 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -1 * self.multiple] == self.actual):  # no. 136
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-1 * self.multiple] == 1 or self.ssc[0][-1 * self.multiple] == self.actual) and \
                        self.ssc[-1 * self.multiple][0] == self.actual \
                        and self.ssc[0][-2 * self.multiple] == self.actual and self.ssc[1 * self.multiple][
                    -2 * self.multiple] == self.actual \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][1 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[0][-3 * self.multiple] == 1 or self.ssc[0][-3 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][-3 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 201
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-1 * self.multiple] == 1 or self.ssc[0][-1 * self.multiple] == self.actual) and \
                        self.ssc[1 * self.multiple][0] == self.actual \
                        and self.ssc[0][-2 * self.multiple] == self.actual and self.ssc[-1 * self.multiple][
                    -2 * self.multiple] == self.actual \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][1 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[0][-3 * self.multiple] == 1 or self.ssc[0][-3 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 202
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[0][1 * self.multiple] == self.actual \
                        and self.ssc[2 * self.multiple][0] == self.actual and self.ssc[2 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][0] == 1 or self.ssc[-1 * self.multiple][0] == self.actual) \
                        and (self.ssc[-1 * self.multiple][2 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][0] == 1 or self.ssc[3 * self.multiple][0] == self.actual) \
                        and (self.ssc[3 * self.multiple][-2 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -2 * self.multiple] == self.actual):  # no. 203
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[0][-1 * self.multiple] == self.actual \
                        and self.ssc[2 * self.multiple][0] == self.actual and self.ssc[2 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][0] == 1 or self.ssc[-1 * self.multiple][0] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][0] == 1 or self.ssc[3 * self.multiple][0] == self.actual) \
                        and (self.ssc[3 * self.multiple][2 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    2 * self.multiple] == self.actual):  # no. 204
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[1 * self.multiple][0] == self.actual \
                        and self.ssc[1 * self.multiple][-2 * self.multiple] == self.actual and \
                        self.ssc[2 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][-3 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 205
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[-1 * self.multiple][0] == self.actual \
                        and self.ssc[-1 * self.multiple][-2 * self.multiple] == self.actual and \
                        self.ssc[-2 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -3 * self.multiple] == self.actual):  # no. 206
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[0][-1 * self.multiple] == self.actual \
                        and self.ssc[2 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[2 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-1 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -1 * self.multiple] == self.actual):  # no. 207
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) and self.ssc[0][1 * self.multiple] == self.actual \
                        and self.ssc[2 * self.multiple][1 * self.multiple] == self.actual and \
                        self.ssc[2 * self.multiple][2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    3 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][1 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    1 * self.multiple] == self.actual):  # no. 208
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[-1 * self.multiple][0] == self.actual \
                        and self.ssc[0][1 * self.multiple] == self.actual and self.ssc[2 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-2 * self.multiple][0] == 1 or self.ssc[-2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-1 * self.multiple][2 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-2 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -2 * self.multiple] == self.actual):  # no. 209
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[-1 * self.multiple][0] == self.actual \
                        and self.ssc[0][-1 * self.multiple] == self.actual and self.ssc[2 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-2 * self.multiple][0] == 1 or self.ssc[-2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][2 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    2 * self.multiple] == self.actual):  # no. 210
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, -1) and self.ss("a", -1, 1) and self.ss("a", 1, 0) and self.ss("a", 1, -2) \
                        and (self.ss("b", 2, -2) or self.ss("b", -2, 2)) \
                        and (self.ss("b", 2, -2) or self.ss("b", -3, 3)) \
                        and (self.ss("b", -2, 2) or self.ss("b", 3, -3)) \
                        and (self.ss("b", 1, 1) or self.ss("b", 1, -3)) \
                        and (self.ss("b", 1, 1) or self.ss("b", 2, -4)) \
                        and (self.ss("b", 1, -3) or self.ss("b", 1, 2)):  # no. 211
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 1, -1) and self.ss("a", -1, 1) and self.ss("a", 2, -1) and self.ss("a", 0, -1) \
                        and (self.ss("b", 2, -2) or self.ss("b", -2, 2)) \
                        and (self.ss("b", 2, -2) or self.ss("b", -3, 3)) \
                        and (self.ss("b", -2, 2) or self.ss("b", 3, -3)) \
                        and (self.ss("b", 3, -1) or self.ss("b", -1, -1)) \
                        and (self.ss("b", 3, -1) or self.ss("b", -2, -1)) \
                        and (self.ss("b", -1, -1) or self.ss("b", 4, -1)):  # no. 212
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, -1) and self.ss("a", 0, 1) and self.ss("a", 1, 0) and self.ss("a", -1, -2) \
                        and (self.ss("b", 0, -2) or self.ss("b", 0, 2)) \
                        and (self.ss("b", 0, -2) or self.ss("b", 0, 3)) \
                        and (self.ss("b", 0, 2) or self.ss("b", 0, -3)) \
                        and (self.ss("b", 2, 1) or self.ss("b", -2, -3)) \
                        and (self.ss("b", 2, 1) or self.ss("b", -3, -4)) \
                        and (self.ss("b", -2, -3) or self.ss("b", 3, 2)):  # no. 213
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, -1) and self.ss("a", 0, 1) and self.ss("a", -1, 0) and self.ss("a", 1, -2) \
                        and (self.ss("b", 0, -2) or self.ss("b", 0, 2)) \
                        and (self.ss("b", 0, -2) or self.ss("b", 0, 3)) \
                        and (self.ss("b", 0, 2) or self.ss("b", 0, -3)) \
                        and (self.ss("b", -2, 1) or self.ss("b", 2, -3)) \
                        and (self.ss("b", -2, 1) or self.ss("b", 3, -4)) \
                        and (self.ss("b", 2, -3) or self.ss("b", -3, 2)):  # no. 214
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, -1) and self.ss("a", 1, 1) and self.ss("a", 0, -1) and self.ss("a", -2, -1) \
                        and (self.ss("b", -2, -2) or self.ss("b", 2, 2)) \
                        and (self.ss("b", -2, -2) or self.ss("b", 3, 3)) \
                        and (self.ss("b", 2, 2) or self.ss("b", -3, -3)) \
                        and (self.ss("b", -3, -1) or self.ss("b", 1, -1)) \
                        and (self.ss("b", -3, -1) or self.ss("b", 2, -1)) \
                        and (self.ss("b", 1, -1) or self.ss("b", -4, -1)):  # no. 215
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, -1) and self.ss("a", 1, 1) and self.ss("a", -1, 0) and self.ss("a", -1, -2) \
                        and (self.ss("b", -2, -2) or self.ss("b", 2, 2)) \
                        and (self.ss("b", -2, -2) or self.ss("b", 3, 3)) \
                        and (self.ss("b", 2, 2) or self.ss("b", -3, -3)) \
                        and (self.ss("b", -1, -3) or self.ss("b", -1, 1)) \
                        and (self.ss("b", -1, -3) or self.ss("b", -1, 2)) \
                        and (self.ss("b", -1, 1) or self.ss("b", -1, -4)):  # no. 216
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 2, 0) and self.ss("a", 1, 0) and self.ss("a", 1, 1) and self.ss("a", 3, -1) \
                        and (self.ss("b", 3, 0) or self.ss("b", -1, 0)) \
                        and (self.ss("b", 3, 0) or self.ss("b", -2, 0)) \
                        and (self.ss("b", -1, 0) or self.ss("b", 4, 0)) \
                        and (self.ss("b", 0, 2) or self.ss("b", 4, -2)) \
                        and (self.ss("b", 0, 2) or self.ss("b", 5, -3)) \
                        and (self.ss("b", 4, -2) or self.ss("b", -1, 3)):  # no. 217
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 2, 0) and self.ss("a", 1, 0) and self.ss("a", 1, -1) and self.ss("a", 3, 1) \
                        and (self.ss("b", 3, 0) or self.ss("b", -1, 0)) \
                        and (self.ss("b", 3, 0) or self.ss("b", -2, 0)) \
                        and (self.ss("b", -1, 0) or self.ss("b", 4, 0)) \
                        and (self.ss("b", 0, -2) or self.ss("b", 4, 2)) \
                        and (self.ss("b", 0, -2) or self.ss("b", 5, 3)) \
                        and (self.ss("b", 4, 2) or self.ss("b", -1, -3)):  # no. 218
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 2, -2) and self.ss("a", 1, -1) and self.ss("a", 2, -1) and self.ss("a", 2, -3) \
                        and (self.ss("b", 3, -3) or self.ss("b", -1, 1)) \
                        and (self.ss("b", 3, -3) or self.ss("b", -2, 2)) \
                        and (self.ss("b", -1, 1) or self.ss("b", 4, -4)) \
                        and (self.ss("b", 2, 0) or self.ss("b", 2, -4)) \
                        and (self.ss("b", 2, 0) or self.ss("b", 2, -5)) \
                        and (self.ss("b", 2, -4) or self.ss("b", 2, 1)):  # no. 219
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -2 * self.multiple] == self.actual) and self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][-2 * self.multiple] == self.actual and \
                        self.ssc[3 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) \
                        and (self.ssc[4 * self.multiple][-2 * self.multiple] == 1 or self.ssc[4 * self.multiple][
                    -2 * self.multiple] == self.actual):  # no. 220
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) and \
                        self.ssc[0][-1 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[-1 * self.multiple][-3 * self.multiple] == self.actual \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[0][-3 * self.multiple] == 1 or self.ssc[0][-3 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][0] == 1 or self.ssc[2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-2 * self.multiple][-4 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -4 * self.multiple] == self.actual):  # no. 221
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) and \
                        self.ssc[0][-1 * self.multiple] == self.actual \
                        and self.ssc[-1 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[1 * self.multiple][-3 * self.multiple] == self.actual \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[0][-3 * self.multiple] == 1 or self.ssc[0][-3 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][0] == 1 or self.ssc[-2 * self.multiple][0] == self.actual) \
                        and (self.ssc[2 * self.multiple][-4 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -4 * self.multiple] == self.actual):  # no. 222
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -2 * self.multiple] == self.actual) and self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[-1 * self.multiple][-2 * self.multiple] == self.actual and \
                        self.ssc[-3 * self.multiple][-2 * self.multiple] == self.actual \
                        and (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[0][-2 * self.multiple] == 1 or self.ssc[0][-2 * self.multiple] == self.actual) \
                        and (self.ssc[-4 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-4 * self.multiple][
                    -2 * self.multiple] == self.actual):  # no. 223
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-2 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -2 * self.multiple] == self.actual) and self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and self.ssc[-2 * self.multiple][-1 * self.multiple] == self.actual and \
                        self.ssc[-2 * self.multiple][-3 * self.multiple] == self.actual \
                        and (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][0] == 1 or self.ssc[-2 * self.multiple][0] == self.actual) \
                        and (self.ssc[-2 * self.multiple][-4 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -4 * self.multiple] == self.actual):  # no. 224
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) and self.ssc[-2 * self.multiple][
                    -2 * self.multiple] == self.actual \
                        and self.ssc[-2 * self.multiple][1 * self.multiple] == self.actual and \
                        self.ssc[-3 * self.multiple][1 * self.multiple] == self.actual \
                        and (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[-3 * self.multiple][3 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    3 * self.multiple] == self.actual) \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[-4 * self.multiple][1 * self.multiple] == 1 or self.ssc[-4 * self.multiple][
                    1 * self.multiple] == self.actual):  # no. 225
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) and self.ssc[2 * self.multiple][2 * self.multiple] == self.actual \
                        and self.ssc[0][1 * self.multiple] == self.actual and self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    3 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][1 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][1 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    1 * self.multiple] == self.actual):  # no. 226
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) and \
                        self.ssc[0][2 * self.multiple] == self.actual \
                        and self.ssc[-1 * self.multiple][2 * self.multiple] == self.actual and \
                        self.ssc[-2 * self.multiple][3 * self.multiple] == self.actual \
                        and (self.ssc[0][-1 * self.multiple] == 1 or self.ssc[0][-1 * self.multiple] == self.actual) \
                        and (self.ssc[0][3 * self.multiple] == 1 or self.ssc[0][3 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) \
                        and (self.ssc[-3 * self.multiple][4 * self.multiple] == 1 or self.ssc[-3 * self.multiple][
                    4 * self.multiple] == self.actual):  # no. 227
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[2 * self.multiple][0] == self.actual \
                        and self.ssc[0][1 * self.multiple] == self.actual and self.ssc[-1 * self.multiple][
                    2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][0] == 1 or self.ssc[-1 * self.multiple][0] == self.actual) \
                        and (self.ssc[3 * self.multiple][0] == 1 or self.ssc[3 * self.multiple][0] == self.actual) \
                        and (self.ssc[2 * self.multiple][-1 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][3 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    3 * self.multiple] == self.actual):  # no. 228
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual) and self.ssc[2 * self.multiple][2 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][2 * self.multiple] == self.actual and \
                        self.ssc[1 * self.multiple][3 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    3 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) \
                        and (self.ssc[1 * self.multiple][4 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    4 * self.multiple] == self.actual):  # no. 229
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[2 * self.multiple][
                    -2 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][0] == self.actual and self.ssc[1 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][-3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    -3 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][2 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    2 * self.multiple] == self.actual) \
                        and (self.ssc[1 * self.multiple][-2 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -2 * self.multiple] == self.actual):  # no. 230
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][0] == 1 or self.ssc[1 * self.multiple][0] == self.actual) and \
                        self.ssc[2 * self.multiple][0] == self.actual \
                        and self.ssc[2 * self.multiple][1 * self.multiple] == self.actual and \
                        self.ssc[3 * self.multiple][2 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][0] == 1 or self.ssc[-1 * self.multiple][0] == self.actual) \
                        and (self.ssc[3 * self.multiple][0] == 1 or self.ssc[3 * self.multiple][0] == self.actual) \
                        and (self.ssc[0][-1 * self.multiple] == 1 or self.ssc[0][-1 * self.multiple] == self.actual) \
                        and (self.ssc[4 * self.multiple][3 * self.multiple] == 1 or self.ssc[4 * self.multiple][
                    3 * self.multiple] == self.actual):  # no. 231
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[0][-1 * self.multiple] == 1 or self.ssc[0][-1 * self.multiple] == self.actual) and \
                        self.ssc[0][-2 * self.multiple] == self.actual \
                        and self.ssc[1 * self.multiple][0] == self.actual and self.ssc[2 * self.multiple][
                    1 * self.multiple] == self.actual \
                        and (self.ssc[0][1 * self.multiple] == 1 or self.ssc[0][1 * self.multiple] == self.actual) \
                        and (self.ssc[0][-3 * self.multiple] == 1 or self.ssc[0][-3 * self.multiple] == self.actual) \
                        and (self.ssc[-1 * self.multiple][-2 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    -2 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][2 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    2 * self.multiple] == self.actual):  # no. 232
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if (self.ssc[1 * self.multiple][-1 * self.multiple] == 1 or self.ssc[1 * self.multiple][
                    -1 * self.multiple] == self.actual) and self.ssc[2 * self.multiple][
                    -2 * self.multiple] == self.actual \
                        and self.ssc[0][-1 * self.multiple] == self.actual and self.ssc[-1 * self.multiple][
                    -1 * self.multiple] == self.actual \
                        and (self.ssc[-1 * self.multiple][1 * self.multiple] == 1 or self.ssc[-1 * self.multiple][
                    1 * self.multiple] == self.actual) \
                        and (self.ssc[3 * self.multiple][3 * self.multiple] == 1 or self.ssc[3 * self.multiple][
                    3 * self.multiple] == self.actual) \
                        and (self.ssc[2 * self.multiple][-1 * self.multiple] == 1 or self.ssc[2 * self.multiple][
                    -1 * self.multiple] == self.actual) \
                        and (self.ssc[-2 * self.multiple][-1 * self.multiple] == 1 or self.ssc[-2 * self.multiple][
                    -1 * self.multiple] == self.actual):  # no. 233
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, -1) and self.ss("a", -2, -2) and self.ss("a", -2, -1) and self.ss("a", -3, -1) \
                        and (self.ss("b", 1, 1) or self.ss("b", -3, -3)) \
                        and (self.ss("b", 1, 1) or self.ss("b", -4, -4)) \
                        and (self.ss("b", -3, -3) or self.ss("b", 2, 2)) \
                        and (self.ss("b", -4, -1) or self.ss("b", 0, -1)) \
                        and (self.ss("b", -4, -1) or self.ss("b", 1, -1))\
                        and (self.ss("b", 0, -1) or self.ss("b", -5, -1)):  # no. 234
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, -1) and self.ss("a", 0, -2) and self.ss("a", -1, 0) and self.ss("a", -2, 1) \
                        and (self.ss("b", 0, 1) or self.ss("b", 0, -3)) \
                        and (self.ss("b", 0, 1) or self.ss("b", 0, -4)) \
                        and (self.ss("b", 0, -3) or self.ss("b", 0, 2)) \
                        and (self.ss("b", -3, 2) or self.ss("b", 1, -2)) \
                        and (self.ss("b", -3, 2) or self.ss("b", 2, -3))\
                        and (self.ss("b", 1, -2) or self.ss("b", -4, 3)):  # no. 235
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, 0) and self.ss("a", -2, 0) and self.ss("a", -2, 1) and self.ss("a", -3, 2) \
                        and (self.ss("b", 1, 0) or self.ss("b", -3, 0)) \
                        and (self.ss("b", 1, 0) or self.ss("b", -4, 0)) \
                        and (self.ss("b", -3, 0) or self.ss("b", 2, 0)) \
                        and (self.ss("b", 0, -1) or self.ss("b", -4, 3)) \
                        and (self.ss("b", 0, -1) or self.ss("b", -5, 4))\
                        and (self.ss("b", -4, 3) or self.ss("b", 1, -2)):  # no. 236
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, -1) and self.ss("a", -2, -2) and self.ss("a", -1, 0) and self.ss("a", -1, 1) \
                        and (self.ss("b", 1, 1) or self.ss("b", -3, -3)) \
                        and (self.ss("b", 1, 1) or self.ss("b", -4, -4)) \
                        and (self.ss("b", -3, -3) or self.ss("b", 2, 2)) \
                        and (self.ss("b", -1, 2) or self.ss("b", -1, -2)) \
                        and (self.ss("b", -1, 2) or self.ss("b", -1, -3))\
                        and (self.ss("b", -1, -2) or self.ss("b", -1, 3)):  # no. 237
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, 1) and self.ss("a", -2, 2) and self.ss("a", -1, 2) and self.ss("a", -1, 3) \
                        and (self.ss("b", 1, -1) or self.ss("b", -3, 3)) \
                        and (self.ss("b", 1, -1) or self.ss("b", -4, 4)) \
                        and (self.ss("b", -3, 3) or self.ss("b", 2, -2)) \
                        and (self.ss("b", -1, 0) or self.ss("b", -1, 4)) \
                        and (self.ss("b", -1, 0) or self.ss("b", -1, 5))\
                        and (self.ss("b", -1, 4) or self.ss("b", -1, -1)):  # no. 238
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", -1, 0) and self.ss("a", -2, 0) and self.ss("a", 0, 1) and self.ss("a", 1, 2) \
                        and (self.ss("b", 1, 0) or self.ss("b", -3, 0)) \
                        and (self.ss("b", 1, 0) or self.ss("b", -4, 0)) \
                        and (self.ss("b", -3, 0) or self.ss("b", 2, 0)) \
                        and (self.ss("b", -2, -1) or self.ss("b", 2, 3)) \
                        and (self.ss("b", -2, -1) or self.ss("b", 3, 4))\
                        and (self.ss("b", 2, 3) or self.ss("b", -3, -2)):  # no. 239
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
                if self.ss("b", 0, 1) and self.ss("a", 0, 2) and self.ss("a", 1, 2) and self.ss("a", 2, 3) \
                        and (self.ss("b", 0, -1) or self.ss("b", 0, 3)) \
                        and (self.ss("b", 0, -1) or self.ss("b", 0, 4)) \
                        and (self.ss("b", 0, 3) or self.ss("b", 0, -2)) \
                        and (self.ss("b", -1, 0) or self.ss("b", 3, 4)) \
                        and (self.ss("b", -1, 0) or self.ss("b", 4, 5))\
                        and (self.ss("b", 3, 4) or self.ss("b", -2, -1)):  # no. 240
                    self.count_dir_score(self.special_score, 0)
                    return self.dir_score
        return self.dir_score

    def count_dir_score(self, new_score_actual, new_score_opponent):
        if self.actual == self.u_id:
            if new_score_actual > self.dir_score:
                self.dir_score = new_score_actual
        else:
            if new_score_opponent > self.dir_score:
                self.dir_score = new_score_opponent

    def square_state(self, game, position, direction):
        if direction == 0:
            if self.y + position < self.grid['y'][0] or self.y + position > self.grid['y'][1]:  # out of grid
                return self.opponent
            if self.x in game and self.y + position in game[self.x]:
                return game[self.x][self.y + position]
        if direction == 1:
            if self.x + position < self.grid['x'][0] or self.x + position > self.grid['x'][1] or self.y + position < \
                    self.grid['y'][0] or \
                    self.y + position > self.grid['y'][1]:  # out of grid
                return self.opponent
            if self.x + position in game and self.y + position in game[self.x + position]:
                return game[self.x + position][self.y + position]
        if direction == 2:
            if self.x + position < self.grid['x'][0] or self.x + position > self.grid['x'][1]:  # out of grid
                return self.opponent
            if self.x + position in game and self.y in game[self.x + position]:
                return game[self.x + position][self.y]
        if direction == 3:
            if self.x + position < self.grid['x'][0] or self.x + position > self.grid['x'][1] or self.y - position < \
                    self.grid['y'][0] or \
                    self.y - position > self.grid['y'][1]:  # out of grid
                return self.opponent
            if self.x + position in game and self.y - position in game[self.x + position]:
                return game[self.x + position][self.y - position]
        return 1

    def square_state_custom(self, game, move_x, move_y):
        if self.x + move_x < self.grid['x'][0] or self.x + move_x > self.grid['x'][1] or self.y + move_y < \
                self.grid['y'][0] or \
                self.y + move_y > self.grid['y'][1]:
            return self.opponent
        if self.x + move_x in game and self.y + move_y in game[self.x + move_x]:
            return game[self.x + move_x][self.y + move_y]
        return 1

    def ss(self, check_type, x, y):
        # check_type ~ b ( both ), a ( actual )
        if check_type == "b":
            return self.ssc[x * self.multiple][y * self.multiple] == 1 or \
                   self.ssc[x * self.multiple][y * self.multiple] == self.actual
        elif check_type == "a":
            return self.ssc[x * self.multiple][y * self.multiple] == self.actual

    def thinking(self, game):
        print('Thinking')
        res = list()
        self.move_no += 1
        # If first move:
        if len(game) == 0:
            res.append(random.randrange(self.grid['x'][0] + 25, self.grid['x'][1] - 25, 3))
            res.append(random.randrange(self.grid['y'][0] + 15, self.grid['y'][1] - 15, 3))
            return [res, 0]

        score_list = list()
        print(game)
        for x, line in game.items():
            for y, square in line.items():
                if square == 1:
                    self.x = x
                    self.y = y
                    self.actual = self.opp_id
                    self.opponent = self.u_id
                    score_opp = self.check_square(game)
                    self.actual = self.u_id
                    self.opponent = self.opp_id
                    score_u = self.check_square(game)
                    if score_u == self.special_score and self.special_score > score_opp > (self.special_score/2):
                        score = score_opp
                    else:
                        score = score_opp + score_u
                    score_list.append({'x': x, 'y': y, 'score': score})
        scores_sorted = sorted(score_list, key=lambda d: d['score'], reverse=True)
        res_scores = list()
        for i in scores_sorted:
            if i['score'] > scores_sorted[0]['score'] - 50:
                res_scores.append(i)
        print(scores_sorted)
        if self.move_no >= 5 and len(res_scores) > 1:
            game_backup = game.copy()
            score_list = list()
            for j in res_scores:
                x = j['x']
                y = j['y']
                game_local = dict()
                for i in {1, 2, 3}:
                    if x + i <= self.grid['x'][1]:
                        if x + i not in game_local:
                            game_local[x + i] = dict()
                        if x + i not in game:
                            game[x + i] = dict()
                        if (y + i not in game[x + i] or game[x + i][y + i] == 1) and y + i <= self.grid['y'][1]:
                            game_local[x + i][y + i] = 1
                        if y not in game[x + i] or game[x + i][y] == 1:
                            game_local[x + i][y] = 1
                        if (y - i not in game[x + i] or game[x + i][y - i] == 1) and y - i >= self.grid['y'][0]:
                            game_local[x + i][y - i] = 1

                    if x - i >= self.grid['x'][0]:
                        if x - i not in game_local:
                            game_local[x - i] = dict()
                        if x - i not in game:
                            game[x - i] = dict()
                        if (y - i not in game_local[x - i] or game[x - i][y - i] == 1) and y - i >= self.grid['y'][0]:
                            game_local[x - i][y - i] = 1
                        if y not in game_local[x - i] or game[x - i][y] == 1:
                            game_local[x - i][y] = 1
                        if (y + i not in game_local[x - i] or game[x - i][y + i] == 1) and y + i <= self.grid['y'][1]:
                            game_local[x - i][y + i] = 1

                    if x not in game:
                        game[x] = dict()
                    if x not in game_local:
                        game_local[x] = dict()
                    if y + i <= self.grid['y'][1]:
                        if y + i not in game_local[x] or game[x][y + i] == 1:
                            game_local[x][y + i] = 1
                    if (y - i not in game[x] or game[x][y - i] == 1) and y - i >= self.grid['y'][0]:
                        game_local[x][y - i] = 1
                for x, line in game_local.items():
                    for y, square in line.items():
                        if square == 1:
                            game = game_backup.copy()
                            tmp = game[j['x']][j['y']]
                            game[j['x']][j['y']] = self.u_id
                            self.x = x
                            self.y = y
                            self.actual = self.opp_id
                            self.opponent = self.u_id
                            score = self.check_square(game)
                            game[j['x']][j['y']] = tmp
                            score_list.append({'x': j['x'], 'y': j['y'], 'score': score})
            scores_sorted = sorted(score_list, key=lambda d: d['score'], reverse=True)
            res_scores = list()
            for i in scores_sorted:
                if i['score'] == scores_sorted[0]['score']:
                    res_scores.append(i)
        print(res_scores)
        random.shuffle(res_scores)
        res.append(res_scores[0]['x'])
        res.append(res_scores[0]['y'])
        return [res, res_scores[0]['score']]
