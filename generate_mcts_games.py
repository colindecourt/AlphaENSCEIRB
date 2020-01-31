import argparse
import numpy as np
import sys

from Go import *
from OnePlaneEncoder import *
from .players import myPlayerUCTS#, myPlayerBasic

def generate_game(board_size, rounds, max_moves, temperature):
    boards, moves = [], []
    encoder = OnePlaneEncoder(board_size)
    game = Go(board_size)
    bot = myPlayerUCTS.myPlayer(board_size)
    num_moves = 0
    while not game.is_game_over():
        print(game)
        move = bot.getPlayerMove()
        (x,y) = move
        nextplayercolor = game._nextPlayer
        if game.is_valid_move(nextplayercolor,[x,y]):
            boards.append(encoder.encode(game))
            move_on_hot = np.zeros(encoder.num_token())
            move_on_hot[encoder.encode(move)]
            moves.append(move_on_hot)
        print(move)
        game.push([nextplayercolor, x, y])
        num_moves += 1
        if num_moves > max_moves:
            break
    return np.array(boards), np.array(moves)