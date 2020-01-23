import numpy as np
import copy

CP = 1/np.sqrt(2)

_BLACK = 1
_WHITE = 2

'''
UCT search based from : 
https://www.labri.fr/perso/lsimon/ia-2019/App-Alphago/MCTS-survey.pdf
page 6-7-8-9
'''
class Node:

    def __init__(self, parent, board):
        self.incoming_action = None
        self.total_sim_reward = 0
        self.visit_count = 0
        self.parent = parent
        self.board = board
        self.children = []

    def choose_untried_action(self, legal_moves):
        """
        Choose randomly a move among legal moves, not in childrens
        :return: a new board with the new move
        """
        children_moves = [c.incoming_action for c in self.children]## NEW
        _legal_moves = []
        for l_m in legal_moves:
            if l_m not in children_moves:
                _legal_moves.append(l_m)
        random_move = np.random.randint(0, len(_legal_moves))
        move = _legal_moves[random_move]
        new_board = copy.deepcopy(self.board)
        new_board.push(move)
        return new_board, move

def tree_policy(v):
    """
        Get tree policy
    :param v: a node
    :return: a node
    """
    is_g_over = v.board.is_game_over()
    legal_moves = v.board.get_legal_moves()
    while not is_g_over:
        if len(v.children) == 0 or len(v.children)<len(legal_moves):## NEW
            return expand(v, legal_moves)
        else:
            v = best_child(v, CP)
        is_g_over = v.board.is_game_over()
        legal_moves = v.board.get_legal_moves()
    return v


def expand(v, legal_moves):
    """
        Chose an action among all possible action and return un new node
    :param v: a node
    :return: the new node
    """
    # False : use the state associated to know node (incoming action variable)
    new_board, action = v.choose_untried_action(legal_moves)
    vp = Node(v, new_board)
    # print('New node', vp)
    # Add new node to v
    vp.incoming_action = action
    v.children.append(vp)
    return vp


def best_child(v, c=CP):
    """
        Return the move associate to the best child
    :param v: node
    :param c: exploitation parameter = 1/sqrt(2)
    :return: best move
    """
    max_score = -np.inf
    best_node = None
    for vp in v.children:
        score = (vp.total_sim_reward/vp.visit_count)+c*np.sqrt((2*np.log(v.visit_count))/vp.visit_count)
        if score > max_score:
            max_score = score
            best_node = vp
            #print("Best score : ", max_score)
    return best_node

def default_policy(s, color):
    """
    :param s: a state
    :return: reward for state s
    """
    # Use all the possible state
    s_copy = copy.deepcopy(s)
    is_game_over = s_copy.is_game_over()
    legal_moves = s_copy.get_legal_moves()
    c = 50
    while not is_game_over:# and c < 50:
        random_move = np.random.randint(0, len(legal_moves))
        move = legal_moves[random_move]
        s_copy.push(move)
        is_game_over = s_copy.is_game_over()
        legal_moves = s_copy.get_legal_moves()
        c += 1

    score = s_copy.get_nb_pieces()[0] - s_copy.get_nb_pieces()[1]
    return -score if color == _BLACK else score


def backup(v, delta):
    """
        Backpropagation function
    :param v: a node
    :param delta:
    :return: parent of node v
    """
    while v is not None:
        v.visit_count += 1
        v.total_sim_reward = v.total_sim_reward + delta
        v = v.parent

def uct_search(board, color=_WHITE, computational_budget = 25):
    v0 = Node(None, board)
    _computational_budget = computational_budget
    while _computational_budget > 0:
        vl = tree_policy(v0)
        delta = default_policy(vl.board, color)
        backup(vl, delta)
        #vtemp = vl
        _computational_budget -= 1
    # print(v0.children)
    return best_child(v0, 0).incoming_action