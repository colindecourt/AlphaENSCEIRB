'''
    Goban utils class and functions
'''
import numpy as np

class Goban:
    def __init__(self, size = 5):
        self._size = size
        self._state = {'B':'X', 'W':'O', '_':'.'}
        self._grid = np.asarray([[self._state['_'] for i in range(self._size)]for j in range(self._size)])

    def get_liberty(self, tk):
        '''
            Return the number of degree of liberty
        '''
        pass

    def get_legal_moves(self, tk):
        '''
            Return an array of legal moves
        '''
        pass

    def get_neighboors(self, tk, pos):
        '''
            Return an array of neighboors
        '''
        l = pos[0]
        c = pos[1]
        neighbors = []
        for L in range(-1,2):
            for C in range(-1,2):
                if L!=0 or C!=0 :
                    if np.abs(L) != np.abs(C):
                        if not(l+L == -1 or l+L > self._size-1 or c+C == -1 or c+C > self._size-1):
                            neighbors.append(np.array([l+L, c+C]))
        return neighbors

    def is_valid(self, pos):
        '''
            Return a bolean that indicate if the move is valid
        '''
        pass

        