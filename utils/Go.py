'''
    Class that implement the game of go.
'''
import numpy as np
import copy

from utils import Token, UnionFind

class Go:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0
    _MAX_MOVE = 300
    def __init__(self, goban_size=9):
        self._nbWHITE = 0
        self._nbBLACK = 0
        self._nextPlayer = self._BLACK
        self._goban_size = goban_size
        self._state = {'B':'X', 'W':'O', '_':'.'}
        self._goban = np.asarray([[self._EMPTY for i in range(self._goban_size)]for j in range(self._goban_size)])
        self._past_goban = np.asarray([])
        self._stack= []
        self._successivePass = 0
        self._nb_move = 0

    def reset(self):
        self.__init__()

    def _flip(self, player):
        if player == self._BLACK:
            return self._WHITE 
        return self._BLACK

    def get_goban_size(self):
        return self._goban_size

    def get_goban(self):
        return self._goban

    def get_goban_state(self, board):
        _boardC = copy.deepcopy(board)
        _boardC[_boardC == self._EMPTY] = self._state['_']
        _boardC[_boardC == self._BLACK] = self._state['B']
        _boardC[_boardC == self._WHITE] = self._state['W']
        return _boardC

    def get_liberty(self, pos):
        """
            Return the number of degree of liberty
        """
        liberty = 0
        neighbors = self.get_neighbors(pos)
        for neigh in neighbors:
            if neigh == self._EMPTY:
                liberty += 1
        return liberty

    def get_legal_moves(self):
        """
            Return an array of legal moves
        """
        legal_moves = []
        for l in range(self._goban_size):
            for c in range(self._goban_size):
                if self._goban[l, c] == self._EMPTY:
                    legal_moves.append([l,c])
        return legal_moves

    def get_neighbors(self, pos):
        """
            Return an array of neighbors
        """
        l = pos[0]
        c = pos[1]
        neighbors = []
        for L in range(-1,2):
            for C in range(-1,2):
                if L!=0 or C!=0 :
                    if np.abs(L) != np.abs(C):
                        if not(l+L == -1 or l+L > self._goban_size-1 or c+C == -1 or c+C > self._goban_size-1):
                            neighbors.append(np.array([l+L, c+C]))
        return neighbors

    def _is_on_board(self, pos):
        return pos[0] >= 0 and pos[0] < self._goban_size-1 and pos[1] >= 0 and pos[1] < self._goban_size-1

    #TO DO
    def _is_never_seen(self, pos, player):
        # self.place_token(pos, player)
        return True

    def _is_valid_move(self, pos, player):
        # verify by hash if the board have been already seen
        isAlreadySeen = not self._is_never_seen(pos, player)
        if isAlreadySeen:
            return False
        else:
            # False if there is already a token or out of the board 
            if not self._is_on_board(pos) or self._goban[pos[0],pos[1]] != self._EMPTY:
                return False
            else:
                return True

    #TO DO
    def capture_token(self):
        pass

    def place_token(self, pos, player):
        self._goban[pos[0],pos[1]] = player

    #TO DO
    def push(self, move):
        # legal_moves = self._goban.get_legal_moves()
        ### Random choice
        # move = legal_moves[np.random.randint(0, legal_moves.count)]
        [player, pos] = [move[0], move[1:]]
        if self._is_valid_move(pos, player):
            self.place_token(pos, player)
        else:
            exp = ""
            raise Exception("Invalid move:"+exp)

    def is_game_over(self):
        if self._nb_move < self._MAX_MOVE:
            self._nbBLACK = self.count_corner(self._BLACK)
            self._nbWHITE = self.count_corner(self._WHITE)
            if self._nbWHITE + self._nbBLACK == (self._goban_size*self._goban_size):
                return True
            else:
                False
        else:
            return True
    def count_corner(self, player) :
        return len(np.where(self._goban == player))

    def _piece2str(self, c):
        if c==self._WHITE:
            return 'O'
        elif c==self._BLACK:
            return 'X'
        else:
            return '.'

    def __str__(self):
        toreturn=""
        for l in self._goban:
            for c in l:
                toreturn += self._piece2str(c)
            toreturn += "\n"
        toreturn += "Next player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + "\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        toreturn += "(successive pass: " + str(self._successivePass) + " )"
        return toreturn

    __repr__ = __str__
