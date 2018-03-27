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
from collections import Counter
from itertools import chain
import math
import logging
from tqdm import tqdm
import matplotlib.pyplot as pyplot
import seaborn as sns
import pandas as pd
from scipy.stats import beta
from utils import Sample
import pdb

class Algorithm(object):
    """
    Base class for MAB algorithms that solve the VLSI allocation problem. 
    
    ...
    
    Parameters
    __________
    sampler_set: SamplerSet
        The SamplerSet used to obtain new samples.
    reward_model: RewardModel
        The RewardModel that is updated as new samples are drawn. The Algorithm uses
        the posterior samples from the RewardModel to make decisions about future sampling
        rates.
    .. todo:: Completing tests 
    """
    def __init__(self, sampler_set, reward_models):
        self.sampler_set = sampler_set
        self.reward_models = reward_models
        self.num_arms = len(self.sampler_set)
        self.best_sample = Sample({}, lambda x: -float('Inf'), lambda x: False)

    def solve(self, num_rounds, samples_per_round):
        """
        Solves the MAB problem for a given budget size and batch size.

        Implementation should generate samples in batches for the specified number of rounds. 
        The reward model is updated every round using past samples. Sampling is then 
        performed as per the implementing algorithm using the updated reward model.
        
        ...

        Parameters
        __________
        num_rounds: int
            The total number of rounds of sampling to perform.
        samples_per_round: int
            The number of samples to draw every round.

        Returns
        _______
        best_sample: 
            The best sample obtained after num_rounds of sampling i.e.
            the sample with the highest reward value
        """
        raise NotImplementedError('Solve not implemented')

class ThompsonSampling(Algorithm):
    def __init__(self, sampler_set, reward_models):
        super(ThompsonSampling, self).__init__(sampler_set, reward_models)
        self.total_count = Counter()
        self.logger = logging.getLogger( 'Thompson Sampling Solver ' + str(id(self)) )
    
    def solve(self, num_rounds, samples_per_round):
        """
        Implements :py:func:`algorithms.Algorithm.solve` according to the Thompson Sampling Algorithm [1]_.
        
        References
        __________

        .. [1] W.R.Thompson. On the likelihood that one unknown probability exceeds another in view of the evidence of two samples. Biometrika, 25(3-4):285-294, 1933.
        """
        for iteration in range(num_rounds):
            # Drawing Samples
            reward_samples = self.reward_models.sample_posterior(samples_per_round)
            sample_counts = Counter(np.argmax(reward_samples, axis = 1))
            self.total_count += sample_counts
            samples = self.sampler_set.get_samples([sample_counts[i] for i in range(len(self.sampler_set))])
            # Updating Reward Models
            for idx, s in enumerate(samples):
                self.reward_models.update(s, idx)
            # Get the new best sample
            valid_samples = filter(lambda x: x.is_valid(), reduce(lambda x, y: x+y, samples))
            self.best_sample = max(valid_samples + [self.best_sample], lambda x: x.get_metric())[0]

        return self.best_sample if self.best_sample.is_valid() else None
    
