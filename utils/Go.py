'''
    Class that implement the game of go.
'''
import numpy as np
import copy

import Token as TK
import UnionFind as UF

class Go:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0
    
    uf = UF.UnionFind()
    def __init__(self, goban_size=9):
        self._nbWHITE = 0
        self._nbBLACK = 0
        self._nextPlayer = self._BLACK
        self._goban_size = goban_size
        self._state = {'B':'X', 'W':'O', '_':'.'}
        self._goban = np.asarray([[TK.Token(name = '{}{}'.format(i,j),color=self._EMPTY) for j in range(self._goban_size)]for i in range(self._goban_size)])
        self._past_goban = []
        self._stack= []
        self._successivePass = 0
        self._nb_move = 0
        self._points = {self._BLACK:0, self._WHITE:0}
        self._MAX_MOVE = goban_size * goban_size * goban_size

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

    def is_uf_liberty(self, tk):
        """
            Return the number of degree of liberty
        """
        liberty = 0
        tk_root = tk.parent
        to_study = [tk_root]
        to_study.extend(tk_root.sons)
        for _tk in to_study:
            _tk_pos = [int(_tk.name[0]),int(_tk.name[1])]
            for _tk_neigh in self.get_neighbors(_tk_pos):
                if self._goban[_tk_neigh[0], _tk_neigh[1]].color == self._EMPTY:
                    liberty += 1

        if liberty == 0:
            return False, to_study
        else:
            return True, to_study

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
        game_copy = copy.deepcopy(self)
        game_copy.push([player, pos[0], pos[1]])
        hashed_goban = hash(str(game_copy._goban))
        if hashed_goban in self._past_goban:
            return False
        else:
            return True

    def is_valid_move(self, player, pos):
        # verify by hash if the board have been already seen
        # False if there is already a token or out of the board 
        if self._is_on_board(pos) and self._goban[pos[0],pos[1]].color == self._EMPTY:
            is_never_seen = self._is_never_seen(pos, player)
            return is_never_seen
        else:
            return False

    #TO DO
    def capture_token(self, to_capture):
        for tk in to_capture:
            tk.__init__(name = tk.name,color=self._EMPTY)
            self._points[self._nextPlayer] +=1
            if self._nextPlayer == self._BLACK:
                self._nbWHITE -= 1
            else:
                self._nbBLACK -= 1

    def place_token(self, pos, player):
        self._goban[pos[0],pos[1]].color = player
        tk_pos_neigh = self.get_neighbors(pos)
        i = 0
        while len(tk_pos_neigh) > 0 and i<len(tk_pos_neigh):
            to_capture = []
            tk_pos = tk_pos_neigh[i]
            tk = self._goban[tk_pos[0],tk_pos[1]]
            if tk.color == player:
                self.uf.union(tk, self._goban[pos[0],pos[1]])
                # Flatten the tree
                [[self.uf.find(tk) for tk in l]for l in self._goban]
            elif tk.color == self._flip(player):
                is_liberty, to_capture = self.is_uf_liberty(tk)
                if not is_liberty:
                    self.capture_token(to_capture)
            else:
                pass
            tk_pos_neigh.pop(i)
            i += 1

        hashed_goban = hash(str(self._goban))
        self._past_goban.append(hashed_goban)
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
        if self._nb_move < self._MAX_MOVE:# and len(legal_moves)!=0:
            if self._nbWHITE + self._nbBLACK >= (self._goban_size*self._goban_size):
                return True
            else:
                return False
        else:
            return True
    def count_corner(self) :
        count_b = 0
        count_w = 0
        for i in range(self._goban_size) :
            for j in range(self._goban_size) :
                if self._goban[i][j].color == self._WHITE :
                    count_w += 1
                elif self._goban[i][j].color == self._BLACK :
                    count_b += 1
        return count_w, count_b

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

    def print_debug(self):
        print("*"*20)
        print(self)
        print("*"*20)

    __repr__ = __str__
