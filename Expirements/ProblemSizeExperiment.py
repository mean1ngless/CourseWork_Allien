import time
import numpy as np
from Distributions.GreedyDistribution import GreedyDistribution
from Distributions.GeneticDistribution import GeneticDistribution
from ProblemGenerator import ProblemGenerator


class ProblemSizeExperiment:
    def __init__(self, item_counts, m, Va, Vb, Wa, Wb, Ng, Np, Mp, Er):
        self.item_counts = item_counts
        self.m = m
        self.Va = Va
        self.Vb = Vb
        self.Wa = Wa
        self.Wb = Wb
        self.Ng = Ng
        self.Np = Np
        self.Mp = Mp
        self.Er = Er
        self.num_experiments = 30

    def run_experiment(self):

        results = {
            'greedy': {
                'volume_diffs': np.zeros(len(self.item_counts)),
                'weight_diffs': np.zeros(len(self.item_counts)),
                'times': np.zeros(len(self.item_counts))
            },
            'genetic': {
                'volume_diffs': np.zeros(len(self.item_counts)),
                'weight_diffs': np.zeros(len(self.item_counts)),
                'times': np.zeros(len(self.item_counts))
            }
        }

        for i, n in enumerate(self.item_counts):
            print(f"Перевіряємо задачу з {n} предметами...")

            for exp in range(self.num_experiments):

                generator = ProblemGenerator(n, self.Va, self.Vb, self.Wa, self.Wb)
                items = generator.generate_as_dicts()

                start_time = time.time()
                greedy = GreedyDistribution(items, self.m)
                _, gr_wdiff, gr_vdiff = greedy.distribute()
                gr_time = time.time() - start_time

                start_time = time.time()
                genetic = GeneticDistribution(
                    items, self.m, self.Np, self.Ng, self.Mp, self.Er
                )
                _, ge_wdiff, ge_vdiff = genetic.evolve()
                ge_time = time.time() - start_time

                results['greedy']['volume_diffs'][i] += gr_vdiff
                results['greedy']['weight_diffs'][i] += gr_wdiff
                results['greedy']['times'][i] += gr_time

                results['genetic']['volume_diffs'][i] += ge_vdiff
                results['genetic']['weight_diffs'][i] += ge_wdiff
                results['genetic']['times'][i] += ge_time

            for algo in ['greedy', 'genetic']:
                for metric in ['volume_diffs', 'weight_diffs', 'times']:
                    results[algo][metric][i] /= self.num_experiments

        return results

    def analyze_results(self, results):
        analysis = {}

        for i, n in enumerate(self.item_counts):
            analysis[n] = {
                'greedy': {
                    'avg_volume_diff': results['greedy']['volume_diffs'][i],
                    'avg_weight_diff': results['greedy']['weight_diffs'][i],
                    'avg_time': results['greedy']['times'][i],
                    'total_diff': results['greedy']['volume_diffs'][i] * results['greedy']['weight_diffs'][i]
                },
                'genetic': {
                    'avg_volume_diff': results['genetic']['volume_diffs'][i],
                    'avg_weight_diff': results['genetic']['weight_diffs'][i],
                    'avg_time': results['genetic']['times'][i],
                    'total_diff': results['genetic']['volume_diffs'][i] * results['genetic']['weight_diffs'][i]
                },
                'improvement_ratio': (
                        (results['greedy']['volume_diffs'][i] + results['greedy']['weight_diffs'][i]) /
                        (results['genetic']['volume_diffs'][i] + results['genetic']['weight_diffs'][i])
                )
            }

        return analysis

    def run_full_experiment(self):

        results = self.run_experiment()
        analysis = self.analyze_results(results)
        return results, analysis