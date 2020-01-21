'''
    Class that implement the game of go.
'''
import numpy as np
import copy

from utils import Token as TK, UnionFind as UF

class Go:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0
    _MAX_MOVE = 300
    uf = UF.UnionFind()
    def __init__(self, goban_size=9):
        self._nbWHITE = 0
        self._nbBLACK = 0
        self._nextPlayer = self._BLACK
        self._goban_size = goban_size
        self._state = {'B':'X', 'W':'O', '_':'.'}
        self._goban = np.asarray([[TK.Token(name = '{}{}'.format(i,j),color=self._EMPTY) for j in range(self._goban_size)]for i in range(self._goban_size)])
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
        _boardC[_boardC.color == self._EMPTY] = self._state['_']
        _boardC[_boardC.color == self._BLACK] = self._state['B']
        _boardC[_boardC.color == self._WHITE] = self._state['W']
        return _boardC

    def get_uf_liberty(self, tk):
        """
            Return the number of degree of liberty
        """
        liberty = 0
        # uf_tree = [[_tk if _tk.parent == tk else None for _tk in l] for l in self._goban]
        # a = []
        # for l in self._goban:
        #     for _tk in l:
        #         if _tk.parent == tk:
        #             a.append(_tk)
        # find an algorithm deg(ab)= deg(a)+deg(b)-2
        pos = [int(tk.name[0]),int(tk.name[1])]
        # def get_liberty(self, pos):
        neighbors = self.get_neighbors(pos)
        for neigh in neighbors:
            if self._goban[neigh[0], neigh[1]].color == self._EMPTY:
                liberty += 1
        return liberty

    def get_legal_moves(self):
        """
            Return an array of legal moves
        """
        legal_moves = []
        for l in range(self._goban_size):
            for c in range(self._goban_size):
                if self.is_valid_move(self._nextPlayer, [l,c]):
                    legal_moves.append([self._nextPlayer, l,c])
        if len(legal_moves) is 0:
            legal_moves = [[self._nextPlayer, -1, -1]]
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
    def get_nb_pieces(self):
      return (self._nbWHITE, self._nbBLACK)
    def _is_on_board(self, pos):
        return pos[0] >= 0 and pos[0] < self._goban_size and pos[1] >= 0 and pos[1] < self._goban_size

    #TO DO
    def _is_never_seen(self, pos, player):
        # self.place_token(pos, player)
        return True

    def is_valid_move(self, player, pos):
        # verify by hash if the board have been already seen
        isAlreadySeen = not self._is_never_seen(pos, player)
        if isAlreadySeen:
            return False
        else:
            # False if there is already a token or out of the board 
            if not self._is_on_board(pos) or self._goban[pos[0],pos[1]].color != self._EMPTY:
                return False
            else:
                return True

    #TO DO
    def capture_token(self):
        pass

    def place_token(self, pos, player):
        self._goban[pos[0],pos[1]].color = player
        tk_pos_neigh = self.get_neighbors(pos)
        to_capture = []
        for tk_pos in tk_pos_neigh:
            tk = self._goban[tk_pos[0],tk_pos[1]]
            if tk.color == player:
                self.uf.union(tk, self._goban[pos[0],pos[1]])
            elif tk.color == self._flip(player):
                if self.get_uf_liberty(tk)==0:
                    print(self)
                    print(player,pos)
                    print(tk_pos)
                    # to_capture.append(tk)
            else:
                pass
        # Flatten the tree
        [[self.uf.find(tk) for tk in l]for l in self._goban]

        if len(to_capture)!=0:
            print(self)
            print(pos)
            self.capture_token()

        if player == self._BLACK:
            self._nbBLACK += 1
            self._nextPlayer = self._WHITE
        else:
            self._nbWHITE += 1
            self._nextPlayer = self._BLACK



    #TO DO
    def push(self, move):
        [player, pos] = [move[0], move[1:]]
        if pos[0]==-1 and pos[1]==-1: # pass
            self._nextPlayer = self._flip(player)
            self._stack.append([move, self._successivePass])
            self._successivePass += 1
        else:
            self._stack.append([move, self._successivePass])
            self._successivePass = 0
            self.place_token(pos, player)

    def is_game_over(self):
        if self._nb_move < self._MAX_MOVE and len(self.get_legal_moves())!=0:
            # self._nbBLACK = self.count_corner(self._BLACK)
            # self._nbWHITE = self.count_corner(self._WHITE)
            if self._nbWHITE + self._nbBLACK == (self._goban_size*self._goban_size):
                return True
            else:
                False
        else:
            return True
    def count_corner(self, player) :
        count = 0
        for i in range(self._goban_size-1) :
            for j in range(self._goban_size-1) :
                if self._goban[i][j].color == player :
                    count += 1
        return count

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
                toreturn += self._piece2str(c.color)
            toreturn += "\n"
        toreturn += "Next player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + "\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        toreturn += "(successive pass: " + str(self._successivePass) + " )"
        return toreturn

    __repr__ = __str__
