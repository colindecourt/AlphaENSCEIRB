'''
    https://fr.wikipedia.org/wiki/Union-find
'''

class UnionFind:
    def __init__(self):
        pass
    # Done in Token class
    # # @staticmethod
    # # def make_set(x):
    # #     x.parent = x
    # #     x.son = x
    # #     x.rang = 0

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
            if xRacine.rang < yRacine.rang:
                xRacine.parent = yRacine
            else:
                yRacine.parent = xRacine
                if xRacine.rang == yRacine.rang:
                    xRacine.rang += 1
        



def run_test():
    from Token import Token
    uf = UnionFind()
    a, b, c, d, e, f = Token('a'), Token('b'), Token('c'), Token('d'), Token('e'), Token('f')
    Tokens = [a,b,c,d,e,f]
    # for tk in Tokens:
    #     uf.make_set(tk)
    
    uf.union(a, b)
    uf.union(a, f)
    uf.union(c, d)
    uf.union(c, e)
    uf.union(a, c)

    # [uf.find(tk) for tk in Tokens]
    # uf.find(d)
    # uf.find(e)
    print('a.rang',a.rang)
    print('c.rang',c.rang)
    # print('e.rang',e.rang)
    print('d.rang',d.rang)
    # print('c.son',c.son)
    # print('e',e)
    # print('c',c)
    print('c.parent',c.parent)
    print('d.parent',d.parent)
    print('e.parent',e.parent)
    # assert a == d.parent
    # assert c.parent == d.parent

# run_test()