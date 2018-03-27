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
from mab.rewards import *
import unittest
import uuid

class DummySample:
    def __init__(self, valid, metric):
        self.metric = metric
        self.valid = valid
        self.id = uuid.uuid4()
    def is_valid(self):
        return self.valid
    def get_metric(self):
        return self.metric

class TestRewards(unittest.TestCase):
    def test_binomial_update(self):
        m = BinomialRewardModel(2)
        samples = [DummySample(True, 0), DummySample(False, 0), DummySample(True, 0)]
        m.update(samples, 1)
        self.assertEqual(m.a[1], 3)
        self.assertEqual(m.b[1], 2)
        self.assertEqual(m.a[0], 1)
        self.assertEqual(m.b[0], 1)

    def test_binomial_sample_posterior(self):
        m = BinomialRewardModel(2)
        x, y = m.sample_posterior(10).shape
        self.assertEqual(x, 10)
        self.assertEqual(y, 2)

    def test_reward_model(self):
        m = RewardModel(2)
        self.assertRaises(NotImplementedError, m.update, [], 1)
        self.assertRaises(NotImplementedError, m.sample_posterior, 5)

    def test_constrained_sample_posterior(self):
        m = ConstrainedRewardModel(5, [1]*5)
        s = m.sample_posterior(10)
        self.assertEqual(s.shape, (10, 5))
        self.assertTrue(np.all(s[:,1:] < s[:, :-1]))
    
    def test_gaussian_sample_posterior_raw(self):
        m = GaussianProcessModel(np.diag([1, 1]), 1, 5, [0, 0], 5)
        v = m.sample_posterior(10)
        self.assertTrue(np.all(v == 1))
        self.assertTrue(v.shape, (10, 5))

    def test_gaussian_sample_posterior(self):
        samples = [DummySample(True, 1), DummySample(False, 9), DummySample(True, 1.1)]
        m = GaussianProcessModel(np.diag([1, 1]), 1, 5, [0, 0], 5)
        m.update(samples, 1)
        v = m.sample_posterior(10)
        self.assertEqual(m.current_maxima, 1.1)
        self.assertTrue(v.shape, (10, 5))

    def test_gaussian_update(self):
        samples = [DummySample(True, 1), DummySample(False, 0.9), DummySample(True, 1.1)]
        m = GaussianProcessModel(np.diag([1, 1]), 1, 5, [0, 0], 5)
        m.update(samples, 1)
        sample_ids = [sample.id for sample in samples]
        self.assertEqual(m.data.keys(), [1])
        for sample in m.data[1]:
            self.assertTrue(sample.id in sample_ids)

if __name__ == '__main__':
    unittest.main()
