# -*- coding: utf-8 -*-

import numpy as np
from GnuGo import GnuGo 

class IllegalMove(Exception): 
    pass



# Class board, that can be copied
class Board:
    _BLACK = 1
    _WHITE = 2
    _EMPTY = 0
    _BOARDSIZE = 9 
    _DEBUG = True

    def __init__(self):
      self._nbWHITE = 0  
      self._nbBLACK = 0
      self._capturedWHITE = 0
      self._capturedBLACK = 0
      self._nextPlayer = self._BLACK
      self._board = np.zeros((Board._BOARDSIZE**2), dtype='int8')
      self._lastPlayerHasPassed = False
      self._gameOver = False
      self._stringUnionFind = np.full((Board._BOARDSIZE**2), -1, dtype='int16')
      self._stringLiberties = np.full((Board._BOARDSIZE**2), -1, dtype='int16')
      self._stringSizes = np.full((Board._BOARDSIZE**2), -1, dtype='int16')
      self._empties = set(range(Board._BOARDSIZE **2))

      #Building fast structures for accessing neighborhood
      self._neighbors = []
      self._neighborsEntries = []
      for nl in [self.getNeighbors(fcoord) for fcoord in range(Board._BOARDSIZE**2)] :
          self._neighborsEntries.append(len(self._neighbors))
          for n in nl:
              self._neighbors.append(n)
          self._neighbors.append(-1) # Sentinelle
      self._neighborsEntries = np.array(self._neighborsEntries, dtype='int16')
      self._neighbors = np.array(self._neighbors, dtype='int8')

    @staticmethod
    def flatten(coord):
        return Board._BOARDSIZE * coord[0] + coord[1]

    @staticmethod
    def unflatten(fcoord):
        return divmod(fcoord, Board._BOARDSIZE)

    @staticmethod
    def flip(player):
        if player == Board._BLACK:
            return Board._WHITE 
        return Board._BLACK

    @staticmethod
    def playerName(player):
        if player == Board._BLACK:
            return "black"
        elif player == Board._WHITE:
            return "white"
        return "???"

    # Used only in init to build the neighborsEntries datastructure
    def getNeighbors(self, fcoord):
        x, y = Board.unflatten(fcoord)
        neighbors = ((x+1, y), (x-1, y), (x, y+1), (x, y-1))
        return [Board.flatten(c) for c in neighbors if self._isOnBoard(c[0], c[1])]

    # for union find structure, recover the number of the current string of stones
    def getStringOfStone(self, fcoord):
        successives = []
        while self._stringUnionFind[fcoord] != -1:
            fcoord = self._stringUnionFind[fcoord]
            successives.append(fcoord)
        if len(successives) > 1:
            for fc in successives[:-1]:
                self._stringUnionFind[fc] = fcoord
        return fcoord
    
    def mergeStringNumber(self, str1, str2):
        #print("merge ", str1, str2)
        self._stringLiberties[str1] += self._stringLiberties[str2]
        self._stringLiberties[str2] = -1
        self._stringSizes[str1] += self._stringSizes[str2]
        self._stringSizes[str2] = -1
        assert self._stringUnionFind[str2] == -1
        self._stringUnionFind[str2] = str1


    def putStone(self, fcoord, color):
        self._board[fcoord] = color
        if self._DEBUG:
            assert fcoord in self._empties
        self._empties.remove(fcoord)
        
        nbEmpty = 0
        nbSameColor = 0
        i = self._neighborsEntries[fcoord]
        while self._neighbors[i] != -1:
            n = self._board[self._neighbors[i]]
            if  n == Board._EMPTY:
                nbEmpty += 1
            elif n == color:
                nbSameColor += 1
            i += 1
        nbOtherColor = 4 - nbEmpty - nbSameColor
        currentString = fcoord
        self._stringLiberties[currentString] = nbEmpty
        self._stringSizes[currentString] = 1

        stringWithNoLiberties = [] # String to capture (if applies)
        i = self._neighborsEntries[fcoord]
        while self._neighbors[i] != -1:
            fn = self._neighbors[i]
            if self._board[fn] == color: # We may have to merge the strings
                stringNumber = self.getStringOfStone(fn)
                self._stringLiberties[stringNumber] -= 1
                if currentString != stringNumber:
                    self.mergeStringNumber(stringNumber, currentString)
                currentString = stringNumber
            elif self._board[fn] != Board._EMPTY: # Other color
                stringNumber = self.getStringOfStone(fn)
                self._stringLiberties[stringNumber] -= 1
                if self._stringLiberties[stringNumber] == 0:
                    if stringNumber not in stringWithNoLiberties: # We may capture more than one string
                        stringWithNoLiberties.append(stringNumber)
            i += 1

        if Board._DEBUG: # Checks that the board is locally consistent
            string, reached = self.breadthSearchStringAndReached(fcoord)
            assert self._board[fcoord] == color
            assertString = self.getStringOfStone(fcoord)
            looseLiberty = 0 # Checks that my liberties are loosely counted
            for fc in string:
                assert assertString == self.getStringOfStone(fc)
                i = self._neighborsEntries[fc] 
                while self._neighbors[i] != -1:
                    fn = self._neighbors[i]
                    assert self._board[fn] == color or fn in reached
                    if self._board[fn] == Board._EMPTY:
                        looseLiberty += 1
                    i += 1
            assert looseLiberty == self._stringLiberties[assertString]
            realLiberty = sum(1 for fc in reached if self._board[fc] == Board._EMPTY)
            assert self._stringLiberties[assertString] >= realLiberty
            assert len(string) == self._stringSizes[assertString]

        return stringWithNoLiberties

    def reset(self):
        self.__init__()


    def _isOnBoard(self,x,y):
        return x >= 0 and x < Board._BOARDSIZE and y >= 0 and y < Board._BOARDSIZE 

    def isSuicide(self, fcoord, color):
        opponent = Board.flip(color)
        i = self._neighborsEntries[fcoord]
        while self._neighbors[i] != -1:
            fn = self._neighbors[i]
            if self._board[fn] != opponent:
                return False
        # Now checks if playing there will take all the neighbors strings

        return True


    # Too costly to be used in all the cases
    def breadthSearchStringAndReached(self, fc):
        color = self._board[fc]
        string = set([fc])
        reached = set()
        frontier = [fc]
        while frontier:
            current_fc = frontier.pop()
            string.add(current_fc)
            i = self._neighborsEntries[current_fc]
            while self._neighbors[i] != -1:
                fn = self._neighbors[i]
                i += 1
                if self._board[fn] == color and not fn in string:
                    frontier.append(fn)
                elif self._board[fn] != color:
                    reached.add(fn)
        return string, reached

    # Too costly to be used in all the cases
    def breadthSearchString(self, fc):
        color = self._board[fc]
        string = set([fc])
        frontier = [fc]
        while frontier:
            current_fc = frontier.pop()
            string.add(current_fc)
            i = self._neighborsEntries[current_fc]
            while self._neighbors[i] != -1:
                fn = self._neighbors[i]
                i += 1
                if self._board[fn] == color and not fn in string:
                    frontier.append(fn)
        return string

    def isGameOver(self):
        return  self._gameOver 

    # Renvoi la liste des coups possibles
    # Note: cette méthode pourrait être codée plus efficacement
    def legalMoves(self):
        moves = []
        return moves

    def _piece2str(self, c):
        if c==self._WHITE:
            return 'O'
        elif c==self._BLACK:
            return 'X'
        else:
            return '.'

    def __str__(self):
        toreturn=""
        for i,c in enumerate(self._board):
            toreturn += self._piece2str(c) + \
                    '('+str(i)+":"+str(self._stringUnionFind[i])+","+str(self._stringLiberties[i])+') '
            if (i+1) % Board._BOARDSIZE == 0:
                toreturn += "\n"
        toreturn += "Next player: " + ("BLACK" if self._nextPlayer == self._BLACK else "WHITE") + "\n"
        toreturn += str(self._nbBLACK) + " blacks and " + str(self._nbWHITE) + " whites on board\n"
        return toreturn

    def prettyPrint(self):
        if Board._BOARDSIZE != 9 and Board._BOARDSIZE != 7:
            print(self)
            return
        print()
        print("To Move: ", "black" if self._nextPlayer == Board._BLACK else "white")
        print()
        print("     WHITE (O) has captured %d stones" % self._capturedBLACK)
        print("     BLACK (X) has captured %d stones" % self._capturedWHITE)
        print()
        if Board._BOARDSIZE == 9:
            specialPoints = [(2,2), (6,2), (4,4), (2,6), (6,6)]
            headerline = "    A B C D E F G H J"
        else:
            specialPoints = [(2,2), (4,2), (3,3), (2,4), (4,4)]
            headerline = "    A B C D E F G"
        print(headerline)
        for l in range(Board._BOARDSIZE):
            line = Board._BOARDSIZE - l
            print("  %d" % line, end="")
            for c in range(Board._BOARDSIZE):
                p = self._board[Board.flatten((l,c))]
                ch = '.'
                if p==Board._WHITE:
                    ch = 'O'
                elif p==Board._BLACK:
                    ch = 'X'
                elif (l,c) in specialPoints:
                    ch = '+'
                print(" " + ch, end="")
            print(" %d" % line)
        print(headerline)

    @staticmethod
    def moveNameToCoord(s):
        indexLetters = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'J':8}

        col = indexLetters[s[0]]
        lin = Board._BOARDSIZE - int(s[1:])
        return (lin, col)

    def captureString(self, fc):
        string = self.breadthSearchString(fc)
        for s in string:
            if self._nextPlayer == Board._WHITE:
                self._capturedBLACK += 1
            else:
                self._capturedWHITE += 1
            self._board[s] = self._EMPTY
            self._empties.add(s)
            i = self._neighborsEntries[s]
            while self._neighbors[i] != -1:
                fn = self._neighbors[i]
                if self._board[fn] != Board._EMPTY:
                    st = self.getStringOfStone(fn)
                    if st != s:
                        self._stringLiberties[st] += 1
                i += 1
            self._stringUnionFind[s] = -1
            self._stringSizes[s] = -1
            self._stringLiberties[s] = -1

    def fullPlayMove(self, fcoord):
        if self._gameOver: return
        if fcoord != -1:
            captured = self.putStone(fcoord, self._nextPlayer)

            # captured is the list of Strings that have 0 liberties
            for fc in captured:
                self.captureString(fc)
        else:
            if self._lastPlayerHasPassed:
                self._gameOver = True
                return
            self._lastPlayerHasPassed = True

        self._nextPlayer = Board.flip(self._nextPlayer)

    def playNamedMove(self, m):
        if m != "PASS":
            self.fullPlayMove(self.flatten(Board.moveNameToCoord(m)))
        else:
            self.fullPlayMove(-1)


board = Board()
board.prettyPrint()
for m in "D4 E4 D3 E5 E6 E7 D2 F6 G7 D6 B2 F5 B3 G5 C2 G6 C3".split():
    board.playNamedMove(m.strip())
    board.prettyPrint()
    print(board)

import sys
sys.exit()

gnugo = GnuGo(Board._BOARDSIZE)
board.prettyPrint()
moves = gnugo.Moves(gnugo)
while not board.isGameOver():
    move = next(moves)
    print("move given by gnugo :", move)
    if move == "ERR": break
    board.playNamedMove(move)
    board.prettyPrint()
    print(board)
    print(gnugo)

print(gnugo.finalScore())

