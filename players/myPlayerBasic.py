# -*- coding: utf-8 -*-

from utils.Go import *
from random import randint

class myPlayer():
    def __init__(self, goban_size = 9):
        self._board = Go(goban_size)
        self._mycolor = None
        self._my_ai = 'Random moves'

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        is_g_over = self._board.is_game_over()
        if is_g_over:
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        moves = self._board.get_legal_moves()
        move = moves[randint(0,len(moves)-1)]
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, [x, y]))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



