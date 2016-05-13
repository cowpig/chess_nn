import chess, chess.pgn
import numpy as np
import sys
import os
import multiprocessing
import itertools
import random
import h5py

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

'''
def parse_games_2(fns_in, fn_out):
    xs = []
    ys = []

    i = 0
    def next_fn(i):
        return fn_out + str(i)

    curr_fn = next_fn(i)

    for fn_in in fns_in:
        for game in read_games(fn_in):
            x, y = parse_game(game)
            xs.extend(x)
            ys.extend(y)

            if len(xs) > 1:
                np.savez(curr_fn, [xs, ys])
                i += 1
                curr_fn = curr_fn(i)

'''

def read_all_games(fn_in, fn_out):
    g = h5py.File(fn_out, 'w')
    x_d = g.create_dataset('x', (0, 64,), dtype='int', maxshape=(None, 64), chunks=True)
    #Y = g.create_dataset('y', (0, len(utils.MOVES)), dtype='bool_', maxshape(None, len(utils.MOVES)), chunks=True)

    size = 0
    for game in read_games(fn_in):
        X,Y = parse_game(game)
        if game is None:
            continue

        g.flush()

        num_rows = len(X)
        new_size = size + num_rows

        print 'resizing to', new_size
        x_d.resize(size=new_size, axis=0)

        for i,s in enumerate(X):
            x_d[size + i] = s

        size = new_size

    g.close()

def read_all_games_2(a):
    return read_all_games(*a)

def parse_dir():
    files = []
    d = 'data'
    for fn_in in os.listdir(d):
        print fn_in
        if not fn_in.endswith('.pgn'):
            continue
        fn_in = os.path.join(d, fn_in)
        fn_out = fn_in.replace('.pgn', '.hdf5')
        if not os.path.exists(fn_out):
            files.append((fn_in, fn_out))

    pool = multiprocessing.Pool()
    pool.map(read_all_games_2, files)
    #map(read_all_games_2, files)

'''
def parse_dir_2(d, fn_out):
    files = []

    for fn_in in os.listdir(d):
        if not fn_in.endswith('.pgn'):
            continue

        print "adding {}".format(fn_in)
        fn_in = os.path.join(d, fn_in)
        files.append(fn_in)

    parse_games_2(files, fn_out)
'''


if __name__ == '__main__':
    parse_dir()
