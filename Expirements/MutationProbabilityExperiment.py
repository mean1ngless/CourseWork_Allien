import numpy as np
from Distributions.GeneticDistribution import GeneticDistribution
from ProblemGenerator import ProblemGenerator


class MutationProbabilityExperiment:
    def __init__(self, A, B, Va, Vb, Wa, Wb, Ng, Np, Er, mutation_probs):
        self.A = A
        self.B = B
        self.Va = Va
        self.Vb = Vb
        self.Wa = Wa
        self.Wb = Wb
        self.Ng = Ng
        self.Np = Np
        self.Er = Er
        self.mutation_probs = mutation_probs
        self.num_experiments = 30

    def run_experiment(self):

        num_a = len(self.A)
        num_b = len(self.B)
        num_mp = len(self.mutation_probs)

        Rv = np.zeros((num_a, num_b, num_mp))
        Rw = np.zeros((num_a, num_b, num_mp))

        for exp in range(self.num_experiments):
            print(f"Експеримент №{exp + 1}/{self.num_experiments}")

            for idx_a, a in enumerate(self.A):
                for idx_b, b in enumerate(self.B):

                    generator = ProblemGenerator(b, self.Va, self.Vb, self.Wa, self.Wb)
                    items = generator.generate_as_dicts()

                    for idx_mp, mp in enumerate(self.mutation_probs):
                        ga = GeneticDistribution(
                            items=items,
                            M=a,
                            Np=self.Np,
                            Ng=self.Ng,
                            Mp=mp,
                            Er=self.Er
                        )

                        _, Wdiff, Vdiff = ga.evolve()

                        Rv[idx_a, idx_b, idx_mp] += Vdiff
                        Rw[idx_a, idx_b, idx_mp] += Wdiff

        Rv /= self.num_experiments
        Rw /= self.num_experiments

        return Rv, Rw

    def analyze_results(self, Rv, Rw):

        analysis = {}

        for idx_a, a in enumerate(self.A):
            for idx_b, b in enumerate(self.B):
                key = f"a={a}, b={b}"
                results = []

                for idx_mp, mp in enumerate(self.mutation_probs):
                    results.append({
                        'mutation_prob': mp,
                        'avg_volume_diff': Rv[idx_a, idx_b, idx_mp],
                        'avg_weight_diff': Rw[idx_a, idx_b, idx_mp],
                        'total_diff': Rv[idx_a, idx_b, idx_mp] + Rw[idx_a, idx_b, idx_mp]
                    })

                optimal_idx = np.argmin([res['total_diff'] for res in results])
                optimal_mp = self.mutation_probs[optimal_idx]

                analysis[key] = {
                    'optimal_mutation_prob': optimal_mp,
                    'detailed_results': results
                }

        return analysis

    def run_full_experiment(self):

        Rv, Rw = self.run_experiment()
        analysis = self.analyze_results(Rv, Rw)
        return Rv, Rw, analysis