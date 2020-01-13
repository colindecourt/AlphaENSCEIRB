class Token:

    def __init__(self, player = 'White'):
        self.player = player
        self.parent = None
        self.son = None