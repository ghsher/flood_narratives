import random

from functools import reduce
from fractions import Fraction
from math import gcd

class FloodModel_1:
    def __init__(self,
                 init_prob=0.1,
                 prob_growth=0.001,
                 prob_growth_2nd=0.0,
                 dist={10   : 0.90090,
                       100  : 0.09009,
                       1000 : 0.00901},
                 seed=None
                ):

        self.prob = init_prob
        self.prob_growth = prob_growth
        self.prob_growth_2nd = prob_growth_2nd

        self.intensity_dist = dist
        self.intensities_list = self.generate_intensities_list()

        if seed == None:
            seed = random.random()
        self.random = random.Random(seed)

        self.floods = []
        self.time = 0
    
    def generate_intensities_list(self):
        intensity_probs = [v for _,v in self.intensity_dist.items()]

        N = reduce(lambda a, b: abs(a * b) // gcd(a, b),
                   (Fraction(f).limit_denominator().denominator for f in intensity_probs))

        intensities = []
        for intensity in self.intensity_dist:
            for i in range(int(N*self.intensity_dist[intensity])):
                intensities.append(intensity)

        return intensities

    def step(self):
        # 1. DETERMINE IF THERE IS A FLOOD
        # TODO: Have this sample from a more intelligent distr (extreme value)?
        #       i.e., be more intelligent than "there exists one probability"
        if self.random.random() < self.prob:
            intensity = self.random.choice(self.intensities_list)
            self.floods.append((self.time, intensity))
        # else:
        #     self.floods.append((self.time, 0))

        # 2. UPDATE FLOOD PROBABILITY FOR NEXT STEP
        self.prob += self.prob_growth
        self.prob_growth += self.prob_growth_2nd

        # 3. ADVANCE TIME
        self.time += 1

# TODO: Extend this to be one FloodModel that has multiple schemes.
#       Allow **kwargs in __init__.

if __name__ == "__main__": 
    model = FloodModel_1(seed=1)
    for i in range(200):
        model.step()
    print(model.floods)