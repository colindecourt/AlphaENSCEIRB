'''
    https://fr.wikipedia.org/wiki/Union-find
'''
from Token import Token
class UnionFind:
    def __init__(self):
        self.a = Token()
        self.b = Token()
        self.c = Token()
        self.d = Token()
        self.e = Token()
        self.f = Token()

    @staticmethod
    def make_set(x):
        x.parent = x
        x.son = x

    @staticmethod
    def find(x):
        if x.parent != x:
            x.parent = UnionFind.find(x.parent)
        return x.parent

    @staticmethod
    def union(x, y):
        xRacine = UnionFind.find(x)
        yRacine = UnionFind.find(y)
        if xRacine != yRacine:
            yRacine.parent = xRacine


def run_test():
    uf = UnionFind()
    uf.union(uf.a, uf.b)
    uf.union(uf.c, uf.d)
    uf.union(uf.a, uf.c)
    assert uf.a == uf.d.parent
    assert uf.c.parent == uf.d.parent

run_test()