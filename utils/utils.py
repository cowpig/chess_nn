import numpy as np
import chess
from itertools import product

# pieces on each sq, whose turn, castling availability, en passant
SQUARES = ["{}{}".format(letter, number) for number in range(8,0,-1) for letter in "abcdefgh"]
PIECES_LOOKUP= {
	"p": 1,
	"P": 2,
	"r": 3,
	"R": 4,
	"n": 5,
	"N": 6,
	"b": 7,
	"B": 8,
	"q": 9,
	"Q": 10,
	"k": 11,
	"K": 12
}
MOVES = None # defined later

# Legal Moves encoding
######################
def sq_number_to_alg(sq_number):
	return SQUARES[sq_number]

def to_alg(sq):
	# assumes a8 is 0 and h1 is 63
	if type(sq) == int:
		return SQUARES[number]
	# assumes a8 is (0,0) and h1 is (7,7)
	elif type(sq) == tuple:
		try:
			return chr(sq[0] + 97) + str(8-sq[1])
		except Exception as e:
			import ipdb; ipdb.set_trace()
	else:
		raise ValueError("to_alg only understands square coord tuples and numbers")

# Legal Moves encoding
######################
def possible_moves():
	def filter_moves(*funcs):
		rngs = [range(8)]*2
		return [(sq1, sq2)
							for sq1, sq2 in product(product(*rngs), product(*rngs))
							if any(func(sq1, sq2) for func in funcs)]

	def is_diagonal((x1, y1), (x2, y2)):
		return (abs(x1 - x2) == abs(y1 - y2)) and x1 != x2

	def is_knight((x1, y1), (x2, y2)):
		return set((1, 2)) == set((abs(x1 - x2), abs(y1 - y2)))

	def is_linear((x1, y1), (x2, y2)):
		return (x1 == x2) != (y1 == y2)

	return ["{}{}".format(to_alg(move[0]), to_alg(move[1])) 
			for move in filter_moves(is_diagonal, is_knight, is_linear)]

MOVES = possible_moves()

# a8 is 0, b8 is 1, ... h1 is 63, to match with FEN notation
def alg_to_sq_number(alg):
	SQUARES_LOOKUP = {alg:ordinal for ordinal, alg in enumerate(SQUARES)}
	return SQUARES_LOOKUP[alg]

def move_idx(move_str):
	return MOVES.index(move_str)

def encode_legal_moves(board):
	# for every square, every other square is possible
	output = np.zeros(len(MOVES))

	for move in board.generate_legal_moves():
		move = str(move)
		if len(move) == 5:
			print move
			move = move[:4]
		output[move_idx(move)] = 1.

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

def en_passant_idx(alg):
	if alg[1] == 6:
		return ord(alg[0]) - 97
	else:
		return ord(alg[0]) - 97 + 8

def bb2array(b, flip=False):
	x = np.zeros(64, dtype=np.int8)

	for piece, pos in get_all_pieces(b):
		if piece != 0:
			col = int(pos % 8)
			row = int(pos / 8)
			if flip:
				row = 7 - row

			x[row * 8 + col] = piece

	return x

def get_all_pieces(board):
	'''
	Returns a list of (piece_type, pos) on a given board
	'''

	fboard = board.fen()
	pieces,_,_,_,_,_ = fboard.split()

	output = []
	pos_idx = 0

	for char in pieces:
		if char.isdigit():
			pos = pos_idx
			pos_idx += int(char)
			for p in range(pos,pos_idx):
				output.append((0,p))

		elif char.isalpha():
			output.append((PIECES_LOOKUP[char], pos_idx))
			pos_idx += 1

	return output

'''
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
		output[N_SQUARES + 6 + en_passant_idx(en_passant)] = 1

	return output
'''

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
