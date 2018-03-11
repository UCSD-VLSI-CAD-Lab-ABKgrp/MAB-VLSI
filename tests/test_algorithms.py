from context import mab
from collections import defaultdict
from mab.algorithms import *
from mab.sampling import Sampler, SamplerSet
from mab.rewards import RewardModel
import unittest

class DummyRewardModel(RewardModel):
    def __init__(self, size):
        super(DummyRewardModel, self).__init__(size)
        self.samples = defaultdict(list)
    def update(self, samples, index):
        self.samples[index] += samples
    def sample_posterior(self, count = 1):
        return np.random.rand(count, self.size)

class DummySampler(Sampler):
    def __init__(self):
        super(DummySampler, self).__init__(['a'], lambda x: 1, lambda x: True, {'b':1})
        self.total_count = 0
        self.loaded_samples = None
    def load_samples(self, samples):
        self.loaded_samples = samples
    def get_samples(self, count = 1):
        self.total_count += count
        if self.loaded_samples == None:
            return map(self.make_sample, [[1]]*count)
        # Repeat samples if count > the number of loaded samples
        return [self.loaded_samples[i%len(self.loaded_samples)] for i in range(count)]

class TestAlgorithms(unittest.TestCase):
    def test_update_samples(self):
        # Test that the number of samples used to update == number of samples drawn at each arm. 
        rm = DummyRewardModel(2)
        smp_set = SamplerSet([DummySampler(), DummySampler()])
        ts = ThompsonSampling(smp_set, rm)
        smp = ts.solve(4, 3)
        for i, s in enumerate(smp_set.samplers):
            self.assertEqual(len(rm.samples[i]), s.total_count)

    def test_best_sample_returned(self):
        """.. todo:: Test that the best out of a set of samples is returned."""
        pass

    def test_only_valid(self):
        """.. todo:: Test only valid samples are considered"""
        pass

    def test_algorithm_properties(self):
        """.. todo:: Testing the algorithm. Weak tests: the better arm is sampled more by margin - XX%, """
        pass
if __name__ == '__main__':
    unittest.main()