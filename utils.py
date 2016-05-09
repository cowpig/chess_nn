import numpy as np
import chess

def letter_to_num(char):
	# a -> 0 ... h -> 8
	return ord(char) - 97

def algebraic_ord(string):
	return 8*letter_to_num(string[0]) + int(string[1]) - 1

def move_ord(move_str):
	start = algebraic_ord(move_str[:2])
	end = algebraic_ord(move_str[2:])

	# remove redundant square-to-itself
	if end > start:
		end -= 1

	return start * 64 + end


def encode_legal_moves(board):
	# for every square, every other square is possible
	output = np.zeros(64 * 63)

	for move in board.legal_moves():
		output[move_ord(str(move))] = 1.

	return output
