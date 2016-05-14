import chess, chess.pgn
import numpy
import sys
import os
import multiprocessing
import itertools
import random

import utils

'''
File I/O utils for the FICS game database.

Source: https://github.com/erikbern/deep-pink
'''

def read_games(fn):
    '''
    Reads in a pgn file from the FICS game database
    (http://www.ficsgames.org/download.html) and returns an iterator of parsed games.
    '''
    f = open(fn)

    while True:
        try:
            g = chess.pgn.read_game(f)
        except KeyboardInterrupt:
            raise
        except:
            continue

        if not g:
            break
        
        yield g

def parse_game(game):
    gn = game.end()

    xs = []
    ys = []
    while gn:
        gn = gn.parent # this mutates gn
        if not gn:
            print "game over"
            break
        b = gn.board()
        x = utils.bb2array(b, flip=(b.turn == 0))
        y = utils.encode_legal_moves(b)
        xs.append(x)
        ys.append(y)

    return (xs, ys)

def read_all_games(fn_in, fn_out):
    xs = []
    ys = []

    i = 0
    pos_count = 0
    next_msg = 1000
    def next_fn(i):
        return fn_out + str(i)

    curr_fn = next_fn(i)

    for game in read_games(fn_in):
        x, y = parse_game(game)
        xs.extend(x)
        ys.extend(y)
        pos_count += len(x)

        if pos_count > next_msg == 0:
            print "parsed {} positions".format(pos_count) 
            next_msg += 1000

        if len(xs) > 500000:
            np.savez(curr_fn, [xs, ys])
            xs = []
            ys = []
            i += 1
            curr_fn = next_fn(i)

def read_all_games_2(a):
    return read_all_games(*a)

def parse_dir(d):
    files = []

    for fn_in in os.listdir(d):
        if not fn_in.endswith('.pgn'):
            continue
        fn_in = os.path.join(d, fn_in)
        fn_out = fn_in.replace('.pgn', '.hdf5')
        if not os.path.exists(fn_out):
            files.append((fn_in, fn_out))

    pool = multiprocessing.Pool()
    pool.map(read_all_games_2, files)

if __name__ == '__main__':
    # try:
    parse_dir("games")
    # except:
    #     print "usage: python parse_game.py <directory_with_pgns> <output_file>"
