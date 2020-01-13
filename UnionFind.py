'''
    https://fr.wikipedia.org/wiki/Union-find
'''
class UnionFind:
    def __init__(self):
        pass

    @staticmethod
    def make_set(x):
        x.parent = None

    @staticmethod
    def find(x):
        if x.parent == None:
            return x
        else:
            return UnionFind.find(x.parent)

    @staticmethod
    def union(x, y):
        xRacine = UnionFind.find(x)
        yRacine = UnionFind.find(y)
        if xRacine != yRacine:
            xRacine.parent = yRacine