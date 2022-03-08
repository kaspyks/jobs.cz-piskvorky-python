#!/usr/bin/python3

import random


def check_square(game, grid, x, y, actual, opponent, u_id):
	max_position = 4
	score = 0
	for direction in (0, 1, 2, 3):
		a_s = dict()  # actual_situation
		dir_score = 0
		for position in range(1, max_position + 1):
			for i in (1, -1):
				a_s[position * i] = square_state(game, x, y, position * i, direction, grid, opponent)
				if not a_s[position * i]:
					a_s[position * i] = 1

		opponent_square_positive = 0
		opponent_square_negative = 0
		free_squares = 1
		for i in range(1, max_position + 1):
			if opponent_square_positive == 0:
				if a_s[i] == opponent:
					opponent_square_positive = 1
				else:
					free_squares += 1
			if opponent_square_negative == 0:
				if a_s[i * (-1)] == opponent:
					opponent_square_negative = 1
				else:
					free_squares += 1
		if free_squares < 5:
			continue

		if a_s[1] == actual:
			if a_s[2] == actual:
				if a_s[3] == actual:
					if a_s[4] == actual or a_s[-1] == actual:  # no. 1, no. 3
						dir_score = count_dir_score(dir_score, actual, u_id, 11000, 10000)
					if a_s[-1] == 1:
						if a_s[4] == 1:  # no. 6
							dir_score = count_dir_score(dir_score, actual, u_id, 1100, 1000)
						if a_s[4] == opponent:  # no. 10
							dir_score = count_dir_score(dir_score, actual, u_id, 100, 150)
				if a_s[-1] == actual:
					if a_s[-2] == actual:  # no. 5
						dir_score = count_dir_score(dir_score, actual, u_id, 11000, 10000)
					if a_s[3] == 1:
						if a_s[-2] == 1:  # no. 8
							dir_score = count_dir_score(dir_score, actual, u_id, 1100, 1000)
						if a_s[-2] == opponent:  # no. 12
							dir_score = count_dir_score(dir_score, actual, u_id, 100, 70)
					if a_s[-2] == 1 and a_s[3] == opponent:  # no. 14
						dir_score = count_dir_score(dir_score, actual, u_id, 100, 120)
				if a_s[3] == 1:
					if a_s[-1] == 1:  # no. 16
						dir_score = count_dir_score(dir_score, actual, u_id, 450, 300)
					if a_s[-1] == opponent:  # no. 19
						dir_score = count_dir_score(dir_score, actual, u_id, 40, 30)
				if a_s[3] == opponent and a_s[-1] == 1:  # no. 22
					dir_score = count_dir_score(dir_score, actual, u_id, 40, 30)
			if a_s[2] == 1:
				if a_s[-1] == 1:  # no. 25
					dir_score = count_dir_score(dir_score, actual, u_id, 11, 10)
					if a_s[-2] == actual and a_s[-3] == 1:  # no. 35
						dir_score = count_dir_score(dir_score, actual, u_id, 240, 80)
				if a_s[-1] == opponent:  # no. 27
					dir_score = count_dir_score(dir_score, actual, u_id, 2, 1)
				if a_s[3] == actual and a_s[-1] == 1 and a_s[4] == 1:   # no. 33
					dir_score = count_dir_score(dir_score, actual, u_id, 240, 80)
			if a_s[2] == opponent and a_s[-1] == 1:  # no. 29
				dir_score = count_dir_score(dir_score, actual, u_id, 2, 1)

		if a_s[-1] == actual:
			if a_s[-2] == actual:
				if a_s[-3] == actual:
					if a_s[-4] == actual or a_s[1] == actual:  # no. 2, no. 4
						dir_score = count_dir_score(dir_score, actual, u_id, 11000, 10000)
					if a_s[1] == 1:
						if a_s[-4] == 1:  # no. 7
							dir_score = count_dir_score(dir_score, actual, u_id, 1100, 1000)
						if a_s[-4] == opponent:  # no. 11
							dir_score = count_dir_score(dir_score, actual, u_id, 100, 150)
				if a_s[1] == actual:
					if a_s[-3] == 1:
						if a_s[2] == 1:  # no. 9
							dir_score = count_dir_score(dir_score, actual, u_id, 1100, 1000)
						if a_s[2] == opponent:  # no. 13
							dir_score = count_dir_score(dir_score, actual, u_id, 100, 70)
					if a_s[-3] == opponent and a_s[2] == 1:  # no. 15
						dir_score = count_dir_score(dir_score, actual, u_id, 100, 120)
				if a_s[1] == 1:
					if a_s[-3] == 1:  # no. 18
						dir_score = count_dir_score(dir_score, actual, u_id, 450, 300)
					if a_s[-3] == opponent:  # no. 21
						dir_score = count_dir_score(dir_score, actual, u_id, 40, 30)
				if a_s[1] == opponent and a_s[-3] == 1:  # no. 24
					dir_score = count_dir_score(dir_score, actual, u_id, 40, 30)
			if a_s[1] == 1:
				if a_s[-2] == 1:  # no. 26
					dir_score = count_dir_score(dir_score, actual, u_id, 11, 10)
					if a_s[2] == actual and a_s[3] == 1:  # no. 36
						dir_score = count_dir_score(dir_score, actual, u_id, 240, 80)
				if a_s[-2] == opponent:  # no. 28
					dir_score = count_dir_score(dir_score, actual, u_id, 2, 1)
			if a_s[1] == opponent and a_s[-2] == 1:  # no. 30
				dir_score = count_dir_score(dir_score, actual, u_id, 2, 1)
			if a_s[-2] == 1 and a_s[-3] == actual and a_s[1] == 1 and a_s[-4] == 1:  # no. 34
				dir_score = count_dir_score(dir_score, actual, u_id, 240, 80)

		if a_s[1] == actual and a_s[-1] == actual:
			if a_s[2] == 1:
				if a_s[-2] == 1:  # no. 17
					dir_score = count_dir_score(dir_score, actual, u_id, 450, 300)
				if a_s[-2] == opponent:  # no. 20
					dir_score = count_dir_score(dir_score, actual, u_id, 40, 30)
			if a_s[2] == opponent and a_s[-2] == 1:  # no. 23
				dir_score = count_dir_score(dir_score, actual, u_id, 40, 30)
		if a_s[1] == 1 and a_s[2] == actual and a_s[3] == actual and a_s[-1] == 1 and a_s[4] == 1:  # no. 31
			dir_score = count_dir_score(dir_score, actual, u_id, 240, 80)
		if a_s[-1] == 1 and a_s[-2] == actual and a_s[-3] == actual and a_s[1] == 1 and a_s[-4] == 1:  # no. 32
			dir_score = count_dir_score(dir_score, actual, u_id, 240, 80)

		score += dir_score

	if score < 500 and actual == u_id:
		ssc = dict()
		for i in range(-5, 5):
			ssc[i] = dict()
			for j in range(-5, 5):
				ssc[i][j] = square_state_custom(game, x, y, i, j, grid, opponent)

		for i in (1, -1):
			if (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) and ssc[1 * i][1 * i] == actual \
				and ssc[2 * i][0] == actual and ssc[1 * i][-1 * i] == actual \
				and (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) \
				and (ssc[3 * i][0] == 1 or ssc[3 * i][0] == actual) \
				and (ssc[1 * i][2 * i] == 1 or ssc[1 * i][2 * i] == actual) \
				and (ssc[1 * i][-2 * i] == 1 or ssc[1 * i][-2 * i] == actual):  # no. 101
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) and ssc[2 * i][0] == actual \
				and ssc[2 * i][-2 * i] == actual and ssc[0][-2 * i] == actual \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][-3 * i] == 1 or ssc[3 * i][-3 * i] == actual) \
				and (ssc[3 * i][1 * i] == 1 or ssc[3 * i][1 * i] == actual) \
				and (ssc[-1 * i][-3 * i] == 1 or ssc[-1 * i][-3 * i] == actual):  # no. 102
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) and ssc[1 * i][-1 * i] == actual \
				and ssc[0][-2 * i] == actual and ssc[-1 * i][-1 * i] == actual \
				and (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) \
				and (ssc[0][-3 * i] == 1 or ssc[0][-3 * i] == actual) \
				and (ssc[2 * i][-1 * i] == 1 or ssc[2 * i][-1 * i] == actual) \
				and (ssc[-2 * i][-1 * i] == 1 or ssc[-2 * i][-1 * i] == actual):  # no. 103
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) and ssc[0][-2 * i] == actual \
				and ssc[-2 * i][-2 * i] == actual and ssc[-2 * i][0] == actual \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) \
				and (ssc[-3 * i][-3 * i] == 1 or ssc[-3 * i][-3 * i] == actual) \
				and (ssc[1 * i][-3 * i] == 1 or ssc[1 * i][-3 * i] == actual) \
				and (ssc[-3 * i][1 * i] == 1 or ssc[-3 * i][1 * i] == actual):  # no. 104
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score

			if (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) and ssc[-1 * i][0] == actual \
				and ssc[1 * i][1 * i] == actual and ssc[1 * i][-1 * i] == actual \
				and (ssc[-2 * i][0] == 1 or ssc[-2 * i][0] == actual) \
				and (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual) \
				and (ssc[1 * i][2 * i] == 1 or ssc[1 * i][2 * i] == actual) \
				and (ssc[1 * i][-2 * i] == 1 or ssc[1 * i][-2 * i] == actual):  # no. 105
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) and ssc[-1 * i][1 * i] == actual \
				and ssc[2 * i][0] == actual and ssc[0][-2 * i] == actual \
				and (ssc[-2 * i][2 * i] == 1 or ssc[-2 * i][2 * i] == actual) \
				and (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual) \
				and (ssc[3 * i][1 * i] == 1 or ssc[3 * i][1 * i] == actual) \
				and (ssc[-1 * i][-3 * i] == 1 or ssc[-1 * i][-3 * i] == actual):  # no. 106
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) and ssc[0][1 * i] == actual \
				and ssc[1 * i][-1 * i] == actual and ssc[-1 * i][-1 * i] == actual \
				and (ssc[0][2 * i] == 1 or ssc[0][2 * i] == actual) \
				and (ssc[0][-2 * i] == 1 or ssc[0][-2 * i][0] == actual) \
				and (ssc[2 * i][-1 * i] == 1 or ssc[2 * i][-1 * i] == actual) \
				and (ssc[-2 * i][-1 * i] == 1 or ssc[-2 * i][-1 * i] == actual):  # no. 107
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) and ssc[1 * i][1 * i] == actual \
				and ssc[0][-2 * i] == actual and ssc[-2 * i][0] == actual \
				and (ssc[2 * i][2 * i] == 1 or ssc[2 * i][2 * i] == actual) \
				and (ssc[-2 * i][-2 * i] == 1 or ssc[-2 * i][-2 * i] == actual) \
				and (ssc[1 * i][-3 * i] == 1 or ssc[1 * i][-3 * i] == actual) \
				and (ssc[-3 * i][1 * i] == 1 or ssc[-3 * i][1 * i] == actual):  # no. 108
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual) and ssc[1 * i][0] == actual \
				and ssc[2 * i][1 * i] == actual and ssc[2 * i][-1 * i] == actual \
				and (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) \
				and (ssc[3 * i][0] == 1 or ssc[3 * i][0] == actual) \
				and (ssc[2 * i][2 * i] == 1 or ssc[2 * i][2 * i] == actual) \
				and (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual):  # no. 109
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual) and ssc[1 * i][-1 * i] == actual \
				and ssc[3 * i][-1 * i] == actual and ssc[1 * i][-3 * i] == actual \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][-3 * i] == 1 or ssc[3 * i][-3 * i] == actual) \
				and (ssc[4 * i][0] == 1 or ssc[4 * i][0] == actual) \
				and (ssc[0][-4 * i] == 1 or ssc[0][-4 * i] == actual):  # no. 110
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual) and ssc[0][-1 * i] == actual \
				and ssc[1 * i][-2 * i] == actual and ssc[-1 * i][-2 * i] == actual \
				and (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) \
				and (ssc[0][-3 * i] == 1 or ssc[0][-3 * i] == actual) \
				and (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual) \
				and (ssc[-2 * i][-2 * i] == 1 or ssc[-2 * i][-2 * i] == actual):  # no. 111
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-2 * i][-2 * i] == 1 or ssc[-2 * i][-2 * i] == actual) and ssc[-1 * i][-1 * i] == actual \
				and ssc[-1 * i][-3 * i] == actual and ssc[-3 * i][-1 * i] == actual \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) \
				and (ssc[-3 * i][-3 * i] == 1 or ssc[-3 * i][-3 * i] == actual) \
				and (ssc[0][-4 * i] == 1 or ssc[0][-4 * i] == actual) \
				and (ssc[-4 * i][0] == 1 or ssc[-4 * i][0] == actual):  # no. 112
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) and ssc[0][2 * i] == actual \
				and ssc[-1 * i][1 * i] == actual and ssc[-2 * i][1 * i] == actual \
				and (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) \
				and (ssc[0][3 * i] == 1 or ssc[0][3 * i] == actual) \
				and (ssc[-3 * i][1 * i] == 1 or ssc[-3 * i][1 * i] == actual) \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual):  # no. 113
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) and ssc[2 * i][2 * i] == actual \
				and ssc[0][2 * i] == actual and ssc[-1 * i][3 * i] == actual \
				and (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) \
				and (ssc[3 * i][3 * i] == 1 or ssc[3 * i][3 * i] == actual) \
				and (ssc[-2 * i][4 * i] == 1 or ssc[-2 * i][4 * i] == actual) \
				and (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual):  # no. 114
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) and ssc[2 * i][0] == actual \
				and ssc[1 * i][1 * i] == actual and ssc[1 * i][2 * i] == actual \
				and (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) \
				and (ssc[3 * i][0] == 1 or ssc[3 * i][0] == actual) \
				and (ssc[1 * i][3 * i] == 1 or ssc[1 * i][3 * i] == actual) \
				and (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual):  # no. 115
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) and ssc[2 * i][-2 * i] == actual \
				and ssc[2 * i][0] == actual and ssc[3 * i][1 * i] == actual \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][-3 * i] == 1 or ssc[3 * i][-3 * i] == actual) \
				and (ssc[4 * i][2 * i] == 1 or ssc[4 * i][2 * i] == actual) \
				and (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual):  # no. 116
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) and ssc[0][-2 * i] == actual \
				and ssc[-1 * i][-1 * i] == actual and ssc[-2 * i][-1 * i] == actual \
				and (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) \
				and (ssc[0][-3 * i] == 1 or ssc[0][-3 * i] == actual) \
				and (ssc[-3 * i][-1 * i] == 1 or ssc[-3 * i][-1 * i] == actual) \
				and (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual):  # no. 117
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) and ssc[-2 * i][-2 * i] == actual \
				and ssc[-2 * i][0] == actual and ssc[-3 * i][1 * i] == actual \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) \
				and (ssc[-3 * i][-3 * i] == 1 or ssc[-3 * i][-3 * i] == actual) \
				and (ssc[-4 * i][2 * i] == 1 or ssc[-4 * i][2 * i] == actual) \
				and (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual):  # no. 118
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) and ssc[-2 * i][0] == actual \
				and ssc[-1 * i][1 * i] == actual and ssc[-1 * i][2 * i] == actual \
				and (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) \
				and (ssc[-3 * i][0] == 1 or ssc[-3 * i][0] == actual) \
				and (ssc[-1 * i][3 * i] == 1 or ssc[-1 * i][3 * i] == actual) \
				and (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual):  # no. 119
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) and ssc[-2 * i][2 * i] == actual \
				and ssc[0][2 * i] == actual and ssc[1 * i][3 * i] == actual \
				and (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) \
				and (ssc[-3 * i][3 * i] == 1 or ssc[-3 * i][3 * i] == actual) \
				and (ssc[2 * i][4 * i] == 1 or ssc[2 * i][4 * i] == actual) \
				and (ssc[-2 * i][0] == 1 or ssc[-2 * i][0] == actual):  # no. 120
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) and ssc[-1 * i][0] == actual \
				and ssc[0][-2 * i] == actual and ssc[1 * i][-2 * i] == actual \
				and (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) \
				and (ssc[-2 * i][1 * i] == 1 or ssc[-2 * i][1 * i] == actual) \
				and (ssc[0][-3 * i] == 1 or ssc[0][-3 * i] == actual) \
				and (ssc[2 * i][-3 * i] == 1 or ssc[2 * i][-3 * i] == actual):  # no. 121
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) and ssc[1 * i][0] == actual \
				and ssc[0][-2 * i] == actual and ssc[-1 * i][-2 * i] == actual \
				and (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) \
				and (ssc[2 * i][1 * i] == 1 or ssc[2 * i][1 * i] == actual) \
				and (ssc[0][-3 * i] == 1 or ssc[0][-3 * i] == actual) \
				and (ssc[-2 * i][-3 * i] == 1 or ssc[-2 * i][-3 * i] == actual):  # no. 122
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) and ssc[0][1 * i] == actual \
				and ssc[2 * i][0] == actual and ssc[2 * i][-1 * i] == actual \
				and (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) \
				and (ssc[-1 * i][2 * i] == 1 or ssc[-1 * i][2 * i] == actual) \
				and (ssc[3 * i][0] == 1 or ssc[3 * i][0] == actual) \
				and (ssc[3 * i][-2 * i] == 1 or ssc[3 * i][-2 * i] == actual):  # no. 123
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) and ssc[0][-1 * i] == actual \
				and ssc[2 * i][0] == actual and ssc[2 * i][1 * i] == actual \
				and (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) \
				and (ssc[-1 * i][-2 * i] == 1 or ssc[-1 * i][-2 * i] == actual) \
				and (ssc[3 * i][0] == 1 or ssc[3 * i][0] == actual) \
				and (ssc[3 * i][2 * i] == 1 or ssc[3 * i][2 * i] == actual):  # no. 124
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) and ssc[1 * i][0] == actual \
				and ssc[1 * i][-2 * i] == actual and ssc[2 * i][-2 * i] == actual \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][-3 * i] == 1 or ssc[3 * i][-3 * i] == actual) \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) \
				and (ssc[1 * i][-3 * i] == 1 or ssc[1 * i][-3 * i] == actual):  # no. 125
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) and ssc[-1 * i][0] == actual \
				and ssc[-1 * i][-2 * i] == actual and ssc[-2 * i][-2 * i] == actual \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) \
				and (ssc[-3 * i][-3 * i] == 1 or ssc[-3 * i][-3 * i] == actual) \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[-1 * i][-3 * i] == 1 or ssc[-1 * i][-3 * i] == actual):  # no. 126
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) and ssc[0][-1 * i] == actual \
				and ssc[2 * i][-1 * i] == actual and ssc[2 * i][-2 * i] == actual \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][-3 * i] == 1 or ssc[3 * i][-3 * i] == actual) \
				and (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) \
				and (ssc[3 * i][-1 * i] == 1 or ssc[3 * i][-1 * i] == actual):  # no. 127
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) and ssc[0][1 * i] == actual \
				and ssc[2 * i][1 * i] == actual and ssc[2 * i][2 * i] == actual \
				and (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) \
				and (ssc[3 * i][3 * i] == 1 or ssc[3 * i][3 * i] == actual) \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][1 * i] == 1 or ssc[3 * i][1 * i] == actual):  # no. 128
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) and ssc[-1 * i][0] == actual \
				and ssc[1 * i][-1 * i] == actual and ssc[1 * i][-2 * i] == actual \
				and (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual) \
				and (ssc[-2 * i][0] == 1 or ssc[-2 * i][0] == actual) \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) \
				and (ssc[1 * i][-3 * i] == 1 or ssc[1 * i][-3 * i] == actual):  # no. 129
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) and ssc[1 * i][0] == actual \
				and ssc[-1 * i][-1 * i] == actual and ssc[-1 * i][-2 * i] == actual \
				and (ssc[-2 * i][0] == 1 or ssc[-2 * i][0] == actual) \
				and (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual) \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[-1 * i][-3 * i] == 1 or ssc[-1 * i][-3 * i] == actual):  # no. 130
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) and ssc[-1 * i][-1 * i] == actual \
				and ssc[0][-2 * i] == actual and ssc[-1 * i][-3 * i] == actual \
				and (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual) \
				and (ssc[-2 * i][2 * i] == 1 or ssc[-2 * i][2 * i] == actual) \
				and (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual) \
				and (ssc[-2 * i][-4 * i] == 1 or ssc[-2 * i][-4 * i] == actual):  # no. 131
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual) and ssc[-1 * i][-1 * i] == actual \
				and ssc[2 * i][0] == actual and ssc[3 * i][1 * i] == actual \
				and (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual) \
				and (ssc[-2 * i][2 * i] == 1 or ssc[-2 * i][2 * i] == actual) \
				and (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual) \
				and (ssc[4 * i][2 * i] == 1 or ssc[4 * i][2 * i] == actual):  # no. 132
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) and ssc[0][1 * i] == actual \
				and ssc[-1 * i][-1 * i] == actual and ssc[-2 * i][-1 * i] == actual \
				and (ssc[0][2 * i] == 1 or ssc[0][2 * i] == actual) \
				and (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual) \
				and (ssc[-3 * i][-1 * i] == 1 or ssc[-3 * i][-1 * i] == actual) \
				and (ssc[1 * i][-1 * i] == 1 or ssc[1 * i][-1 * i] == actual):  # no. 133
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-1 * i] == 1 or ssc[0][-1 * i] == actual) and ssc[0][1 * i] == actual \
				and ssc[1 * i][-1 * i] == actual and ssc[2 * i][-1 * i] == actual \
				and (ssc[0][2 * i] == 1 or ssc[0][2 * i] == actual) \
				and (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual) \
				and (ssc[3 * i][-1 * i] == 1 or ssc[3 * i][-1 * i] == actual) \
				and (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual):  # no. 134
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) and ssc[1 * i][1 * i] == actual \
				and ssc[-2 * i][0] == actual and ssc[-3 * i][1 * i] == actual \
				and (ssc[-2 * i][-2 * i] == 1 or ssc[-2 * i][-2 * i] == actual) \
				and (ssc[2 * i][2 * i] == 1 or ssc[2 * i][2 * i] == actual) \
				and (ssc[-4 * i][2 * i] == 1 or ssc[-4 * i][2 * i] == actual) \
				and (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual):  # no. 135
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) and ssc[-1 * i][-1 * i] == actual \
				and ssc[0][2 * i] == actual and ssc[-1 * i][3 * i] == actual \
				and (ssc[2 * i][2 * i] == 1 or ssc[2 * i][2 * i] == actual) \
				and (ssc[-2 * i][-2 * i] == 1 or ssc[-2 * i][-2 * i] == actual) \
				and (ssc[-2 * i][4 * i] == 1 or ssc[-2 * i][4 * i] == actual) \
				and (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual):  # no. 136
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[2 * i][0] == 1 or ssc[2 * i][0] == actual) and ssc[1 * i][0] == actual \
				and ssc[2 * i][-1 * i] == actual and ssc[2 * i][-2 * i] == actual \
				and (ssc[-1 * i][0] == 1 or ssc[-1 * i][0] == actual) \
				and (ssc[3 * i][0] == 1 or ssc[3 * i][0] == actual) \
				and (ssc[2 * i][1 * i] == 1 or ssc[2 * i][1 * i] == actual) \
				and (ssc[2 * i][-3 * i] == 1 or ssc[2 * i][-3 * i] == actual):  # no. 137
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-2 * i][0] == 1 or ssc[-2 * i][0] == actual) and ssc[-1 * i][0] == actual \
				and ssc[-2 * i][-1 * i] == actual and ssc[-2 * i][-2 * i] == actual \
				and (ssc[1 * i][0] == 1 or ssc[1 * i][0] == actual) \
				and (ssc[-3 * i][0] == 1 or ssc[-3 * i][0] == actual) \
				and (ssc[-2 * i][1 * i] == 1 or ssc[-2 * i][1 * i] == actual) \
				and (ssc[-2 * i][-3 * i] == 1 or ssc[-2 * i][-3 * i] == actual):  # no. 138
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual) and ssc[1 * i][-1 * i] == actual \
				and ssc[1 * i][-3 * i] == actual and ssc[0][-4 * i] == actual \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][-3 * i] == 1 or ssc[3 * i][-3 * i] == actual) \
				and (ssc[-1 * i][5 * i] == 1 or ssc[-1 * i][5 * i] == actual) \
				and (ssc[3 * i][-1 * i] == 1 or ssc[3 * i][-1 * i] == actual):  # no. 139
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[2 * i][-2 * i] == 1 or ssc[2 * i][-2 * i] == actual) and ssc[1 * i][-1 * i] == actual \
				and ssc[3 * i][-1 * i] == actual and ssc[4 * i][0] == actual \
				and (ssc[-1 * i][1 * i] == 1 or ssc[-1 * i][1 * i] == actual) \
				and (ssc[3 * i][-3 * i] == 1 or ssc[3 * i][-3 * i] == actual) \
				and (ssc[5 * i][1 * i] == 1 or ssc[5 * i][1 * i] == actual) \
				and (ssc[1 * i][-3 * i] == 1 or ssc[1 * i][-3 * i] == actual):  # no. 140
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual) and ssc[0][-1 * i] == actual \
				and ssc[-1 * i][-2 * i] == actual and ssc[-2 * i][-2 * i] == actual \
				and (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) \
				and (ssc[0][-3 * i] == 1 or ssc[0][-3 * i] == actual) \
				and (ssc[-3 * i][-2 * i] == 1 or ssc[-3 * i][-2 * i] == actual) \
				and (ssc[1 * i][-2 * i] == 1 or ssc[1 * i][-2 * i] == actual):  # no. 141
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[0][-2 * i] == 1 or ssc[0][-2 * i] == actual) and ssc[0][-1 * i] == actual \
				and ssc[1 * i][-2 * i] == actual and ssc[2 * i][-2 * i] == actual \
				and (ssc[0][1 * i] == 1 or ssc[0][1 * i] == actual) \
				and (ssc[0][-3 * i] == 1 or ssc[0][-3 * i] == actual) \
				and (ssc[3 * i][-2 * i] == 1 or ssc[3 * i][-2 * i] == actual) \
				and (ssc[-1 * i][-2 * i] == 1 or ssc[-1 * i][-2 * i] == actual):  # no. 142
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[-2 * i][-2 * i] == 1 or ssc[-2 * i][-2 * i] == actual) and ssc[-1 * i][-1 * i] == actual \
				and ssc[-3 * i][-1 * i] == actual and ssc[-4 * i][0] == actual \
				and (ssc[1 * i][1 * i] == 1 or ssc[1 * i][1 * i] == actual) \
				and (ssc[-3 * i][-3 * i] == 1 or ssc[-3 * i][-3 * i] == actual) \
				and (ssc[-5 * i][1 * i] == 1 or ssc[-5 * i][1 * i] == actual) \
				and (ssc[-1 * i][-3 * i] == 1 or ssc[-1 * i][-3 * i] == actual):  # no. 143
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
			if (ssc[2 * i][2 * i] == 1 or ssc[2 * i][2 * i] == actual) and ssc[1 * i][1 * i] == actual \
				and ssc[1 * i][3 * i] == actual and ssc[0][4 * i] == actual \
				and (ssc[-1 * i][-1 * i] == 1 or ssc[-1 * i][-1 * i] == actual) \
				and (ssc[3 * i][3 * i] == 1 or ssc[3 * i][3 * i] == actual) \
				and (ssc[-1 * i][5 * i] == 1 or ssc[-1 * i][5 * i] == actual) \
				and (ssc[3 * i][1 * i] == 1 or ssc[3 * i][1 * i] == actual):  # no. 144
				score = count_dir_score(score, actual, u_id, 500, 0)
				return score
	return score


def count_dir_score(dir_score, actual, u_id, new_score_actual, new_score_opponent):
	if actual == u_id:
		if new_score_actual > dir_score:
			dir_score = new_score_actual
	else:
		if new_score_opponent > dir_score:
			dir_score = new_score_opponent
	return dir_score


def square_state(game, x, y, position, direction, grid, opponent):
	if direction == 0:
		if y + position < grid['y'][0] or y + position > grid['y'][1]:  # out of grid
			return opponent
		if x in game and y + position in game[x]:
			return game[x][y + position]
	if direction == 1:
		if x + position < grid['x'][0] or x + position > grid['x'][1] or y + position < grid['y'][0] or \
			y + position > grid['y'][1]:  # out of grid
			return opponent
		if x + position in game and y + position in game[x + position]:
			return game[x + position][y + position]
	if direction == 2:
		if x + position < grid['x'][0] or x + position > grid['x'][1]:  # out of grid
			return opponent
		if x + position in game and y in game[x + position]:
			return game[x + position][y]
	if direction == 3:
		if x + position < grid['x'][0] or x + position > grid['x'][1] or y - position < grid['y'][0] or \
			y - position > grid['y'][1]:  # out of grid
			return opponent
		if x + position in game and y - position in game[x + position]:
			return game[x + position][y - position]
	return 1


def square_state_custom(game, x, y, move_x, move_y, grid, opponent):
	if x + move_x < grid['x'][0] or x + move_x > grid['x'][1] or y + move_y < grid['y'][0] or y + move_y > grid['y'][1]:
		return opponent
	if x + move_x in game and y + move_y in game[x + move_x]:
		return game[x + move_x][y + move_y]
	return 1


def thinking(game, grid, u_id, opp_id):
	print('Thinking')
	res = list()
	# If first move:
	if len(game) == 0:
		res.append(random.randrange(grid['x'][0] + 25, grid['x'][1] - 25, 3))
		res.append(random.randrange(grid['y'][0] + 15, grid['y'][1] - 15, 3))
		return res

	score_list = list()
	for x, line in game.items():
		for y, square in line.items():
			if square == 1:
				score = 0
				score = score + check_square(game, grid, x, y, u_id, opp_id, u_id)
				score = score + check_square(game, grid, x, y, opp_id, u_id, u_id)
				score_list.append({'x': x, 'y': y, 'score': score})
	scores_sorted = sorted(score_list, key=lambda d: d['score'], reverse=True)
	print(scores_sorted)
	res_scores = list()
	for i in scores_sorted:
		if i['score'] == scores_sorted[0]['score']:
			res_scores.append(i)
	random.shuffle(res_scores)
	res.append(res_scores[0]['x'])
	res.append(res_scores[0]['y'])
	return res
