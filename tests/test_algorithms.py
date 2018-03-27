#                             MAB-VLSI 
#
#                           Copyright 2018 
#   Regents of the University of California 
#                         All Rights Reserved
#
#                         
#  MAB-VLSI was developed by Shriram Kumar and Tushar Shah ai at
#  University of California, San Diego.
#
#  If your use of this software contributes to a published paper, we
#  request that you cite our paper that appears on our website 
#  http://vlsicad.ucsd.edu/MAB/MAB_v7.pdf
#
#  Permission to use, copy, and modify this software and its documentation is
#  granted only under the following terms and conditions.  Both the
#  above copyright notice and this permission notice must appear in all copies
#  of the software, derivative works or modified versions, and any portions
#  thereof, and both notices must appear in supporting documentation.
#
#  This software may be distributed (but not offered for sale or transferred
#  for compensation) to third parties, provided such third parties agree to
#  abide by the terms and conditions of this notice.
#
#  This software is distributed in the hope that it will be useful to the
#  community, but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

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