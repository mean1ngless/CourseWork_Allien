import numpy as np
from Distributions.GeneticDistribution import GeneticDistribution
from ProblemGenerator import ProblemGenerator


class TerminationConditionExperiment:
    def __init__(self, n, m, Va, Vb, Wa, Wb, Np, Mp, Er, generations_list):

        self.n = n
        self.m = m
        self.Va = Va
        self.Vb = Vb
        self.Wa = Wa
        self.Wb = Wb
        self.Np = Np
        self.Mp = Mp
        self.Er = Er
        self.generations_list = generations_list
        self.num_experiments = 30

    def run_experiment(self):

        Rv = np.zeros(len(self.generations_list))
        Rw = np.zeros(len(self.generations_list))

        counts = np.zeros(len(self.generations_list))

        for exp in range(self.num_experiments):

            generator = ProblemGenerator(self.n, self.Va, self.Vb, self.Wa, self.Wb)
            items = generator.generate_as_dicts()

            for i, ng in enumerate(self.generations_list):

                ga = GeneticDistribution(items, self.m, Np=self.Np, Ng=ng, Mp=self.Mp, Er=self.Er)

                _, Wdiff, Vdiff = ga.evolve()

                Rv[i] += Vdiff
                Rw[i] += Wdiff
                counts[i] += 1

        Rv /= counts
        Rw /= counts

        return Rv, Rw

    def run_and_analyze(self):
        Rv, Rw = self.run_experiment()

        analysis_results = []
        for i, ng in enumerate(self.generations_list):
            analysis_results.append({
                'generations': ng,
                'avg_volume_diff': Rv[i],
                'avg_weight_diff': Rw[i],
                'total_diff': Rv[i] * Rw[i]
            })

        optimal_idx = np.argmin([res['total_diff'] for res in analysis_results])
        optimal_generations = self.generations_list[optimal_idx]

        return optimal_generations, analysis_results