from context import sample
from sample.rewards import *
import unittest

class DummySample:
    def __init__(self, valid):
        self.valid = valid
    def is_valid(self):
        return self.valid

class TestRewards(unittest.TestCase):
    def test_binomial_update(self):
        m = BinomialRewardModel(2)
        samples = [DummySample(True), DummySample(False), DummySample(True)]
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
        m = ConstrainedRewardModel(5)
        s = m.sample_posterior(10)
        self.assertEqual(s.shape, (10, 5))
        self.assertTrue(np.all(s[:,1:] < s[:, :-1]))
    
    def test_gaussian_sample_posterior(self):
        samples = [[1.1, 2], [0.1]]
        m = GaussianProcessModel(np.diag([1, 1]), 1, 5, [0, 0], 5)
        m.update(samples)
        s = m.sample_posterior(10)
        self.assertTrue(s[m.mean_name].shape, (10, 5))
        self.assertTrue(s[m.std_name].shape, (10, 5))

    def test_gaussian_update(self):
        pass

if __name__ == '__main__':
    unittest.main()
