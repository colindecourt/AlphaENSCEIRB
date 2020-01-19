'''
    https://fr.wikipedia.org/wiki/Union-find
'''

class UnionFind:
    def __init__(self):
        pass

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
    from Token import Token
    uf = UnionFind()
    a, b, c, d, e, f = Token(), Token(), Token(), Token(), Token(), Token()
    Tokens = [a,b,c,d,e,f]
    for tk in Tokens:
        uf.make_set(tk)
    
    uf.union(a, b)
    uf.union(c, d)
    uf.union(a, c)
    uf.find(d)
    assert a == d.parent
    assert c.parent == d.parent

# run_test()