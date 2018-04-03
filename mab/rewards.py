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

import numpy as np
from scipy.stats import beta, t
import random
import uuid
import os
from collections import defaultdict
from scipy.stats import norm

class RewardModel(object):
    """
    The base class for reward models that can be used by the MAB-VLSI algorithms.
    All implementations should override both update and sample_posterior.

    ...
    
    Attributes
    __________
    size: int
        The dimension of samples that the reward model can digest. This is also the
        dimension of posterior samples it produces.
    """
    def __init__(self, size):
        self.size = size

    def update(self, samples, index):
        """
        The function that takes a list of `~utils.Sample`s and updates one dimension
        of the reward model. 
        
        ...
        
        Parameters
        __________
        samples: list
            The set of samples to update the model with. 
        index: int
            The dimension that the smaples should update.
        """
        raise NotImplementedError('Update not implemented')

    def sample_posterior(self, count = 1):
        """
        Generate samples from the current posterior distribution of the rewards.

        Each sample is of dimension size. These samples are used by the Thompson
        Sampling algorithm to choose an arm to play at each step.
        
        ...
        
        Parameters
        __________
        count: int
            The number of samples to draw from the posterior.
        """
        raise NotImplementedError('Sample posterior not implemented')

class BinomialRewardModel(RewardModel):
    """
    Implementation of the :py:class:`rewards.RewardModel` interface for Binomial data. Uses 
    Beta distributions to form a model of the success probability at each arm.
    """
    def __init__(self, size):
        super(BinomialRewardModel, self).__init__(size)
        self.a = np.ones((size,))
        self.b = np.ones((size,))

    def update(self, samples, index):
        self.a[index] += sum(map(lambda x: x.is_valid(), samples))
        self.b[index] += sum(map(lambda x: not x.is_valid(), samples))

    def sample_posterior(self, count = 1):
        return beta.rvs(self.a, self.b, size = (count, self.size))

class ConstrainedRewardModel(BinomialRewardModel):
    """
    An extension of the BinomialRewardModel to take into account decreasing probability
    contraints. 

    These contraints arise naturally in some settings such as increasing clock periods 
    in VLSI designs. When applicable, the constraints can help reduce sample complexity 
    dramatically and should be used.
    """
    def __init__(self, size, reward_values, max_iter = 5):
        super(ConstrainedRewardModel, self).__init__(size)
        self.max_iter = max_iter
        self.reward_values = reward_values

    def get_truncated_sample(self):
        # Inverse sampling
        get_with_default = lambda x, y: y if np.isnan(x) else x 
        inv_sample = lambda a, b, l, u: beta.ppf(random.uniform(beta.cdf(l, a, b), beta.cdf(u, a, b)), a, b)
        sample = [np.nan]*self.size
        l, u = 0, np.inf
        for idx, (a, b) in enumerate(zip(self.a, self.b)*self.max_iter):
            index = idx%self.size
            u = np.inf if index == 0 else sample[index- 1] ### Check logic here
            l = 0 if index == self.size - 1 else get_with_default(sample[index + 1], 0)
            sample[index] = inv_sample(a, b, l, u)
        return [s*r for s, r in zip(sample, self.reward_values)]

    def sample_posterior(self, count = 1):
        return np.array([self.get_truncated_sample() for i in range(count)])

class GaussianProcessModel(RewardModel):
    """
    Implementation of the :py:class:`rewards.RewardModel` interface using a Gaussian Process reward model.
    
    The assumption here is that nearby arms will behave more similarly that arms that are farther
    apart, in terms of metrics. The Gaussian Process model helps enforce this smoothness.
    
    ...

    Attributes
    __________
    K0: 2d array
        A 2d kernel matrix. This controls the amount of smoothness that the model assumes apriori.
    m0: 1d array
        The prior reward means that the model assumes.
    For more details about other parameters, see `this gaussian process tutorial <http://www.gaussianprocess.org/#tut/>`_.
    
    """    
    mean_name = "mu"
    std_name = "sigma"

    def __init__(self, K0, a, b, m0, prec0, sample_burn = 100, sample_thin = 3, sample_tune = 1500):
        super(GaussianProcessModel, self).__init__(len(m0))
        os.environ["THEANO_FLAGS"] = "base_compiledir=~/.theano/" + str(uuid.uuid4())
        import pymc3 as pm
        self.pm = pm
		
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
        self.current_maxima = -np.inf

    def update(self, data, index):
        '''Updates are performed lazily. Data is just stored into a local buffer when update is called'''
        self.data[index] += data
        self.current_maxima = max(self.current_maxima, *map(lambda x: x.get_metric(), filter(lambda x: x.is_valid(), data)))

    def push_updates(self):
		with self.pm.Model() as model:
			sigma = self.pm.Gamma(self.std_name, alpha = self.a, beta = self.b, shape=self.size)
			mu = self.pm.MvNormal(self.mean_name, mu = self.m0, cov = self.kernel, shape=self.size)
			x_ = [self.pm.Normal('x' + str(i), mu[i], sigma[i], observed = map(lambda x: x.get_metric(), self.data[i])) for i in range(self.size)]
			self.posterior_model = model
    
    def sample_posterior(self, count = 1):
        self.push_updates()
        with self.posterior_model:
            trace_ = self.pm.sample(self.sample_thin*count + self.sample_burn, njobs=1, progressbar=False, tune=self.sample_tune)
        samples = trace_[self.sample_burn::self.sample_thin]
        return norm.sf(self.current_maxima, loc = samples[self.mean_name], scale = samples[self.std_name])
