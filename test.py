import numpy as np
import copy

_BLACK = 1
_WHITE = 2
_EMPTY = 0


def __init__(size = 9):
    _size = size
    _state = {'B':'X', 'W':'O', '_':'.'}
    _board = np.asarray([[_EMPTY for i in range(_size)]for j in range(_size)],dtype='object')
    _board[0,0] = _BLACK
    return _board, _state

def get_goban_state(board):
    _boardC = copy.deepcopy(board)
    _boardC[_boardC == _EMPTY] = _state['_']
    _boardC[_boardC == _BLACK] = _state['B']
    _boardC[_boardC == _WHITE] = _state['W']
    return _boardC

_board, _state = __init__()
# print(_board)
print(get_goban_state(_board))