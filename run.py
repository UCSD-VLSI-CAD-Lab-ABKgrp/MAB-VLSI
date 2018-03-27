#                             MAB-VLSI 
#
#         					Copyright 2018 
#  	Regents of the University of California 
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

from mab.rewards import *
from mab.sampling import *
from mab.algorithms import *

SIZE = 3

# Define the reward model.
reward_model = BinomialRewardModel(SIZE)

# Create the sampler objects.
samplers = [GaussianSampler(['a'], lambda x: x['a'], lambda x: x['a'] > 1, {'b': 1}, [1], [1])]*SIZE
sampler_set = SamplerSet(samplers)

# Create the solver and solve for a given budget.
ts_solver = ThompsonSampling(sampler_set, reward_model)
optimal_sample = ts_solver.solve(10, 10)

print "Best sample has metric value: " + str(optimal_sample.get_metric())
