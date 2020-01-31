import Encoder
import Token
class OnePlaneEncoder():
    def __init__(self, board_size):
        self.board_width, self.board_height = board_size
        self.num_planes = 1
    def name(self):
        return 'oneplane'
    def encode(self, game_state):
        board_matrix = np.zeros(self.shape())
        next_player = game_state._nextPlayer
        for r in range(self.board_height):
            for c in range(self.board_width):
                token = game_state._goban[r,c]
                if token.color == next_player:
                    board_matrix[0, r, c] = 1
                else:
                    board_matrix[0, r, c] = -1
        return board_matrix

    def encode_token(self, move):
        return self.board_width * move[0]+move[1]

    def decode_token_index(self, index):
        row = index // self.board_width
        col = index % self.board_width
        return row, col

    def num_token(self):
        return self.board_width * self.board_height

    def shape(self):
        return self.num_planes, self.board_height, self.board_width