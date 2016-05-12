import chess, chess.pgn
import numpy
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

    gs = []
    while gn:
        gn = gn.parent # this mutates gn
        if not gn:
            print "game over"
            break
        b = gn.board()
        s = utils.bb2array(b, flip=(b.turn == 0))
        gs.append(s)

    return gs

def read_all_games(fn_in, fn_out):
    g = h5py.File(fn_out, 'w')
    X = g.create_dataset('x', (0, 64), dtype='b', maxshape=(None, 64), chunks=True)
    size = 0
    line = 0
    for game in read_games(fn_in):
        game = parse_game(game)
        if game is None:
            continue

        if line + 1 >= size:
            g.flush()
            size = 2 * size + 1
            print 'resizing to', size
            X.resize(size=size, axis=0)

        X[line] = game
        line += 1

    X.resize(size=line, axis=0)
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

    #pool = multiprocessing.Pool()
    #pool.map(read_all_games_2, files)
    map(read_all_games_2, files)

if __name__ == '__main__':
    parse_dir()
