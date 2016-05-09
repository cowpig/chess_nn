import chess, chess.pgn
import numpy
import sys
import os
import multiprocessing
import itertools
import random
import h5py

'''

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


def parse_game(g):
    '''
    Returns some sort of object that we'll convert to hdf5 later on
    '''
    pass

def read_all_games(fn_in, fn_out):    
    for game in read_games(fn_in):
        import pdb; pdb.set_trace()
        print game

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
