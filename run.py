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
