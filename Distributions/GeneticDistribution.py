import random
import numpy as np
from copy import deepcopy


class GeneticDistribution:
    def __init__(self, items, M, Np=50, Ng=100, Mp=0.1, Er=0.2, epsilon=1e-6):

        self.items = items
        self.M = M
        self.N = len(items)
        self.Np = Np
        self.Ng = Ng
        self.Mp = Mp
        self.Er = Er
        self.epsilon = epsilon
        self.elite_size = int(Np * Er)

    def create_individual(self):

        individual = np.zeros((self.M, self.N), dtype=int)
        for j in range(self.N):
            i = random.randint(0, self.M - 1)
            individual[i][j] = 1
        return individual

    def initialize_population(self):

        return [self.create_individual() for _ in range(self.Np)]

    def fitness(self, individual):

        weights = np.zeros(self.M)
        volumes = np.zeros(self.M)

        for i in range(self.M):
            for j in range(self.N):
                if individual[i][j] == 1:
                    weights[i] += self.items[j]['weight']
                    volumes[i] += self.items[j]['volume']

        Wdiff = np.max(weights) - np.min(weights) if self.M > 1 else 0
        Vdiff = np.max(volumes) - np.min(volumes) if self.M > 1 else 0

        return (Wdiff + self.epsilon) * (Vdiff + self.epsilon)

    def tournament_selection(self, population, fitnesses, tournament_size=3):

        selected = random.sample(range(len(population)), tournament_size)
        selected_fitnesses = [fitnesses[i] for i in selected]
        winner = selected[np.argmin(selected_fitnesses)]
        return population[winner]

    def crossover(self, parent1, parent2):

        crossover_point = random.randint(1, self.N - 1)
        child1 = np.hstack((parent1[:, :crossover_point], parent2[:, crossover_point:]))
        child2 = np.hstack((parent2[:, :crossover_point], parent1[:, crossover_point:]))
        return child1, child2

    def mutate(self, individual):

        for i in range(self.M):
            for j in range(self.N):
                if random.random() < self.Mp:

                    individual[:, j] = 0
                    new_hand = random.randint(0, self.M - 1)
                    individual[new_hand][j] = 1
        return individual

    def evolve(self):

        population = self.initialize_population()

        for generation in range(self.Ng):

            fitnesses = [self.fitness(ind) for ind in population]

            sorted_pop = [x for _, x in sorted(zip(fitnesses, population), key=lambda pair: pair[0])]

            new_population = deepcopy(sorted_pop[:self.elite_size])

            while len(new_population) < self.Np:
                parent1 = self.tournament_selection(population, fitnesses)
                parent2 = self.tournament_selection(population, fitnesses)

                child1, child2 = self.crossover(parent1, parent2)

                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                if self.fitness(child1) < self.fitness(child2):
                    new_population.append(child1)
                else:
                    new_population.append(child2)

            population = new_population

        best_individual = min(population, key=self.fitness)


        weights = np.zeros(self.M)
        volumes = np.zeros(self.M)

        for i in range(self.M):
            for j in range(self.N):
                if best_individual[i][j] == 1:
                    weights[i] += self.items[j]['weight']
                    volumes[i] += self.items[j]['volume']

        Wdiff = np.max(weights) - np.min(weights) if self.M > 1 else 0
        Vdiff = np.max(volumes) - np.min(volumes) if self.M > 1 else 0

        return best_individual, Wdiff, Vdiff