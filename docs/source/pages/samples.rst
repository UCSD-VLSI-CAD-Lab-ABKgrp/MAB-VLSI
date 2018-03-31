Sample Usage
============

The :file:`run.py` is a sample usage of the MAB-VLSI code to solve a toy Multi Armed Bandit problem. We will go over the various code sections and highlight how this can be used on a real MAB problem.

First the reward model is instantiated.
.. code-block:: python
	reward_model = BinomialRewardModel(SIZE)

Various reward models are available for use in the  :py:mod:`mab.rewards`. Any of these reward modules can be used here. Details about the parameters of individual reward models can be found in the code documentation section. Typically, for Problem 1 as mentioned in our paper, :py:class:`mab.rewards.BinomialRewardModel` will be used and for Problem 2, :py:class:`mab.rewards.GaussianProcessModel` will be used.

Next, the sampler and sampler sets are created. This is the interface that allows the MAB code to draw samples.  

.. code-block:: python
	samplers = [GaussianSampler(['a'], lambda x: x['a'], lambda x: x['a'] > 1, {'b': 1}, [1], [1])]*SIZE
	sampler_set = SamplerSet(samplers)

In this example, samples are simulated from a gaussian distribution. Most real runs will use the :py:class:`mab.sampling.ToolSampler`. 

Finally, the solver is instantiated and solve is called to run the MAB algorithm for a desired schedule and obtain the optimal sample. 

.. code-block:: python
	ts_solver = ThompsonSampling(sampler_set, reward_model)
	optimal_sample = ts_solver.solve(10, 10)