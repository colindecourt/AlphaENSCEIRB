class Token:
    def __init__(self, name, color=None):
        self.name = name
        self.color = color
        self.parent = self
        self.sons = []
        self.rang = 0

    def __str__(self):
        return 'TK({})'.format(self.name)

    __repr__ = __str__