'''
    Class that implement the game of go.
'''
import numpy as np

from Goban import Goban
from Token import Token
from UnionFind import UnionFind as uf

class Go:

    def __init__(self):
        self.goban = Goban()

    def capture_token(self):
        pass
    def place_token(self, pos):
        legal_moves = self.goban.get_legal_moves()
        ### Random choice
        move = legal_moves[np.random.randint(0, legal_moves.count)]
        pass
    def mcts(self):
        pass
