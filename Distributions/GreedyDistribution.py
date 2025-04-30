import math


class GreedyDistribution:
    def __init__(self, items, M, epsilon=1e-6):

        self.items = items
        self.M = M
        self.epsilon = epsilon
        self.N = len(items)
        self.x = [[0 for _ in range(self.N)] for _ in range(M)]
        self.hands = [{'weight': 0, 'volume': 0} for _ in range(M)]

    def calculate_differences(self):

        weights = [hand['weight'] for hand in self.hands]
        volumes = [hand['volume'] for hand in self.hands]

        Wdiff = max(weights) - min(weights) if weights else 0
        Vdiff = max(volumes) - min(volumes) if volumes else 0

        return Wdiff, Vdiff

    def distribute(self):

        for j in range(self.N):
            item = self.items[j]
            min_c = math.inf
            best_hand_idx = 0

            Wdiff, Vdiff = self.calculate_differences()

            for i in range(self.M):

                temp_weight = self.hands[i]['weight'] + item['weight']
                temp_volume = self.hands[i]['volume'] + item['volume']


                temp_weights = [hand['weight'] for idx, hand in enumerate(self.hands) if idx != i] + [temp_weight]
                temp_volumes = [hand['volume'] for idx, hand in enumerate(self.hands) if idx != i] + [temp_volume]


                Wdiff_new = max(temp_weights) - min(temp_weights) if temp_weights else 0
                Vdiff_new = max(temp_volumes) - min(temp_volumes) if temp_volumes else 0


                delta_w = (Wdiff_new - Wdiff) / (Wdiff + self.epsilon)
                delta_v = (Vdiff_new - Vdiff) / (Vdiff + self.epsilon)

                c_i = delta_w + delta_v

                if c_i < min_c:
                    min_c = c_i
                    best_hand_idx = i


            self.x[best_hand_idx][j] = 1
            self.hands[best_hand_idx]['weight'] += item['weight']
            self.hands[best_hand_idx]['volume'] += item['volume']


        final_Wdiff, final_Vdiff = self.calculate_differences()

        return self.x, final_Wdiff, final_Vdiff
