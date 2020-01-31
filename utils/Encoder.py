class Encoder:
    def name(self):
        raise NotImplementedError()

    def encode(self, game_state):
        raise NotImplementedError()

    def encode_token(self, token):
        raise NotImplementedError()

    def decode_token_index(self, index):
        raise NotImplementedError()

    def num_tokens(self):
        raise NotImplementedError()

    def shape(self):
        raise NotImplementedError()