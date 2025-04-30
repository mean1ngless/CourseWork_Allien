import random


class ProblemGenerator:
    def __init__(self, n, Va, Vb, Wa, Wb):

        self.n = n
        self.Va = Va
        self.Vb = Vb
        self.Wa = Wa
        self.Wb = Wb

    def generate(self):

        V = []
        W = []

        for _ in range(self.n):

            volume = random.uniform(self.Va, self.Vb)
            V.append(volume)

            weight = random.uniform(self.Wa, self.Wb)
            W.append(weight)

        return V, W

    def generate_as_dicts(self):

        V, W = self.generate()
        items = [{'volume': v, 'weight': w} for v, w in zip(V, W)]
        return items