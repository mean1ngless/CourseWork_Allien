import numpy as np
from Distributions.GeneticDistribution import GeneticDistribution
from ProblemGenerator import ProblemGenerator


class TerminationConditionExperiment:
    def __init__(self, n, m, Va, Vb, Wa, Wb, Mp, Er, A, B):

        self.n = n
        self.m = m
        self.Va = Va
        self.Vb = Vb
        self.Wa = Wa
        self.Wb = Wb
        self.Mp = Mp
        self.Er = Er
        self.A = A
        self.B = B
        self.num_experiments = 30

    def calculate_iterations(self, a, b):

        return int(a * self.n + b * self.m)

    def run_experiment(self):

        Rv = np.zeros((len(self.A), len(self.B)))
        Rw = np.zeros((len(self.A), len(self.B)))
        counts = np.zeros((len(self.A), len(self.B)))

        for exp in range(self.num_experiments):

            generator = ProblemGenerator(self.n, self.Va, self.Vb, self.Wa, self.Wb)
            items = generator.generate_as_dicts()

            for i, a in enumerate(self.A):
                for j, b in enumerate(self.B):

                    iterations = self.calculate_iterations(a, b)

                    ga = GeneticDistribution(
                        items,
                        self.m,
                        Np=50,
                        Ng=iterations,
                        Mp=self.Mp,
                        Er=self.Er
                    )
                    _, Wdiff, Vdiff = ga.evolve()

                    Rv[i, j] += Vdiff
                    Rw[i, j] += Wdiff
                    counts[i, j] += 1

        Rv /= counts
        Rw /= counts

        return Rv, Rw

    def run_and_analyze(self):

        Rv, Rw = self.run_experiment()

        product_matrix = Rv * Rw

        analysis_results = []
        for i, a in enumerate(self.A):
            for j, b in enumerate(self.B):
                iterations = self.calculate_iterations(a, b)
                analysis_results.append({
                    'a': a,
                    'b': b,
                    'iterations': iterations,
                    'avg_volume_diff': Rv[i, j],
                    'avg_weight_diff': Rw[i, j],
                    'total_diff': product_matrix[i, j]
                })

        min_idx = np.unravel_index(np.argmin(product_matrix), product_matrix.shape)
        optimal_a = self.A[min_idx[0]]
        optimal_b = self.B[min_idx[1]]
        optimal_iterations = self.calculate_iterations(optimal_a, optimal_b)

        return {
            'optimal_a': optimal_a,
            'optimal_b': optimal_b,
            'optimal_iterations': optimal_iterations,
            'volume_diff_matrix': Rv,
            'weight_diff_matrix': Rw,
            'product_matrix': product_matrix,
            'detailed_results': analysis_results
        }