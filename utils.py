import numpy as np
import chess

# pieces on each sq, whose turn, castling availability, en passant
POSITION_SIZE = (6*2 + 1) * 64 + 2 + 4 + 64
MOVES_SIZE = 64 * 63
SQUARES = ["{}{}".format(letter, number) for number in range(8,0,-1) for letter in "abcdefgh"]
MOVES = ["{}{}".format(start, dest) for start in SQUARES for dest in SQUARES if start != dest]

# Legal Moves encoding
######################
def sq_number_to_alg(sq_number):
	return SQUARES[sq_number]

# a8 is 0, b8 is 1, ... h1 is 63, to match with FEN notation
def alg_to_sq_number(alg):
	SQUARES_LOOKUP = {alg:ordinal for ordinal, alg in enumerate(SQUARES)}
	return SQUARES_LOOKUP[alg]

def move_idx(move_str):
	start = alg_to_sq_number(move_str[:2])
	end = alg_to_sq_number(move_str[2:])

	# remove redundant square-to-itself
	if end > start:
		end -= 1

	return start * 63 + end

def encode_legal_moves(board):
	# for every square, every other square is possible
	output = np.zeros(MOVES_SIZE)

	for move in board.generate_legal_moves():
		output[move_idx(str(move))] = 1.

	return output

def sort_decode_moves(moves_vec):
	return sorted(zip(MOVES, moves_vec), lambda a,b: int(b[1]-a[1]*10000))

# Position Encoding
####################

def piece_ord(piece_str):
	piece_ords = {
		'p':0,
		'r':1,
		'n':2,
		'b':3,
		'q':4,
		'k':5,
	}
	if (piece_str.islower()):
		return piece_ords[piece_str] + 6

	return piece_ords[piece_str.lower()]

def pos_idx(sq_number, piece_str=None):
	piece_idx = 0 if piece_str else piece_ord(piece_str) + 1
	return 13*sq_number + piece_idx

def encode_position(board):
	fen = board.fen()
	position,color,castling,en_passant,_,_  = fen.split()

	N_SQUARES = (6*2 + 1) * 64

	# each possible piece + one space for empty for each chess square,
	# plus castling options
	output = np.zeros(POSITION_SIZE)

	sq_number = 0
	for char in position:
		if char.isdigit():
			sq_number += int(char)
		elif char.isalpha():
			output[pos_idx(sq_number, char)] = 1.
			sq_number += 1

	if color == 'w':
		ouptut[N_SQUARES] = 1
	else:
		output[N_SQUARES+1] = 1

	if "K" in castling:
		output[N_SQUARES + 2] = 1
	elif "Q" in castling:
		output[N_SQUARES + 3] = 1
	elif "k" in castling:
		output[N_SQUARES + 4] = 1
	elif "q" in castling:
		output[N_SQUARES + 5] = 1 

	if en_passant != "-":
		output[N_SQUARES + 6 + alg_to_sq_number(en_passant)] = 1

	return output

def test():
	b = chess.Board()
	assert(sum(encode_position(b)) == 32)

	assert(alg_to_sq_number('a8') == 0)
	assert(alg_to_sq_number('b8') == 1)
	assert(alg_to_sq_number('g1') == 62)
	assert(alg_to_sq_number('h1') == 63)

	assert(MOVES.index('a1b2') == move_idx('a1b2'))
	assert(MOVES.index('c3h8') == move_idx('c3h8'))
	assert(MOVES.index('b7g2') == move_idx('b7g2'))
	assert(MOVES.index('d6e4') == move_idx('d6e4'))
