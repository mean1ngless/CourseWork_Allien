import numpy as np
from Distributions.GeneticDistribution import GeneticDistribution
from ProblemGenerator import ProblemGenerator


class MutationProbabilityExperiment:
    def __init__(self, n, m, Va, Vb, Wa, Wb, Ng, Np, Er, mutation_probs):
        self.n = n
        self.m = m
        self.Va = Va
        self.Vb = Vb
        self.Wa = Wa
        self.Wb = Wb
        self.Ng = Ng
        self.Np = Np
        self.Er = Er
        self.mutation_probs = mutation_probs
        self.num_experiments = 10

    def run_experiment(self):

        Rv = np.zeros(len(self.mutation_probs))
        Rw = np.zeros(len(self.mutation_probs))

        for exp in range(self.num_experiments):

            generator = ProblemGenerator(self.n, self.Va, self.Vb, self.Wa, self.Wb)
            items = generator.generate_as_dicts()

            for i, mp in enumerate(self.mutation_probs):

                ga = GeneticDistribution(
                    items=items,
                    M=self.m,
                    Np=self.Np,
                    Ng=self.Ng,
                    Mp=mp,
                    Er=self.Er
                )

                _, Wdiff, Vdiff = ga.evolve()

                Rv[i] += Vdiff
                Rw[i] += Wdiff

        Rv /= self.num_experiments
        Rw /= self.num_experiments

        return Rv, Rw

    def analyze_results(self, Rv, Rw):

        results = []
        for i, mp in enumerate(self.mutation_probs):
            results.append({
                'mutation_prob': mp,
                'avg_volume_diff': Rv[i],
                'avg_weight_diff': Rw[i],
                'total_diff': Rv[i] + Rw[i]
            })

        optimal_idx = np.argmin([res['total_diff'] for res in results])
        optimal_mp = self.mutation_probs[optimal_idx]

        return {
            'optimal_mutation_prob': optimal_mp,
            'detailed_results': results
        }

    def run_full_experiment(self):

        Rv, Rw = self.run_experiment()
        analysis = self.analyze_results(Rv, Rw)
        return Rv, Rw, analysis
