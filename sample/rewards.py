import numpy as np
from scipy.stats import beta, t
import random
import pdb
import uuid
import os
from collections import defaultdict

class RewardModel(object):
    def __init__(self, size):
        self.size = size

    def update(self, samples, index):
        raise NotImplementedError('Update not implemented')

    def sample_posterior(self, count = 1):
        raise NotImplementedError('Sample posterior not implemented')

class BinomialRewardModel(RewardModel):
    def __init__(self, size):
        super(BinomialRewardModel, self).__init__(size)
        self.a = np.ones((size,))
        self.b = np.ones((size,))

    def update(self, samples, index):
        self.a[index] += sum(map(lambda x: x.is_valid(), samples))
        self.b[index] += len(samples) - self.a[index] + 1

    def sample_posterior(self, count = 1):
        return beta.rvs(self.a, self.b, size = (count, self.size))

class ConstrainedRewardModel(BinomialRewardModel):
    def __init__(self, size, max_iter = 5):
        super(ConstrainedRewardModel, self).__init__(size)
        self.max_iter = max_iter

    def get_truncated_sample(self):
        # Inverse sampling
        get_with_default = lambda x, y: y if np.isnan(x) else x 
        inv_sample = lambda a, b, l, u: beta.ppf(random.uniform(beta.cdf(l, a, b), beta.cdf(u, a, b)), a, b)
        sample = [np.nan]*self.size
        l, u = 0, np.inf
        for idx, (a, b) in enumerate(zip(self.a, self.b)*self.max_iter):
            index = idx%self.size
            u = np.inf if index == 0 else sample[index- 1]
            l = 0 if index == self.size - 1 else get_with_default(sample[index + 1], 0)
            sample[index] = inv_sample(a, b, l, u)
        return sample

    def sample_posterior(self, count = 1):
        return np.array([self.get_truncated_sample() for i in range(count)])

class GaussianProcessModel(RewardModel):
    mean_name = "mu"
    std_name = "sigma"

    def __init__(self, K0, a, b, m0, prec0, sample_burn = 100, sample_thin = 3, sample_tune = 1500):
        os.environ["THEANO_FLAGS"] = "base_compiledir=~/.theano/" + str(uuid.uuid4())
        import pymc3 as pm
        self.pm = pm
        self.size = len(m0)
		
        # Setting prior parameters
        self.kernel = prec0*K0
        self.a = a
        self.b = b
        self.m0 = m0

	    # Set some parameters for pymc3
        self.sample_burn = sample_burn
        self.sample_thin = sample_thin
        self.sample_tune = sample_tune
		
        self.posterior_model = pm.Model()
        self.data = defaultdict(list)

    def update(self, data):
		for index, data in enumerate(data):
			self.data[index] += data

		with self.pm.Model() as model:
			sigma = self.pm.Gamma(self.std_name, alpha = self.a, beta = self.b, shape=self.size)
			mu = self.pm.MvNormal(self.mean_name, mu = self.m0, cov = self.kernel, shape=self.size)
			x_ = [self.pm.Normal('x' + str(i), mu[i], sigma[i], observed = self.data[i]) for i in range(self.size)]
			self.posterior_model = model
    
    def sample_posterior(self, sample_size):
        with self.posterior_model:
            #step = pm.Metropolis()
            trace_ = self.pm.sample(self.sample_thin*sample_size + self.sample_burn, njobs = 1, progressbar=True, tune = self.sample_tune)
        return trace_[self.sample_burn::self.sample_thin]

if __name__ == '__main__':
    samples = [[1.1, 2], [0.1]]
    c = GaussianProcessModel(np.diag([1, 1]), 1, 5, [0, 0], 5)
    c.update(samples)
    print c.sample_posterior(10)
