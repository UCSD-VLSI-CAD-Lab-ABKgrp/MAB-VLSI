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

from context import mab
from mab.sampling import *
from mab.utils import GaussianNoiseModel
import unittest
import random
from mock import MagicMock
import pdb
import numpy as np

class TestSamplers(unittest.TestCase):
	def test_base_sampler_make(self):
		random_attributes = ["random_name0", "random_name1"]
		random_constants = {'constant1': 1}
		random_metric = lambda x: sum(x.values())
		random_values = [random.random(), random.random()]
		sampler = Sampler(random_attributes, random_metric, lambda x: True, random_constants)
		sample = sampler.make_sample(random_values)
		self.assertEqual(len(sample.attributes), len(random_attributes) + 1)
		for name in sample.attributes.keys():
			self.assertTrue(name in random_attributes or name in random_constants)
		self.assertEqual(round(sample.get_metric(), 3), round(sum(random_values) + 1, 3))

	def test_base_sampler_get(self):
		random_attributes = ["random_name0", "random_name1"]
		random_constants = {'constant1': 1}
		random_metric = lambda x: sum(x.values())
		random_values = [random.random(), random.random()]
		sampler = Sampler(random_attributes, random_metric, lambda x: True, random_constants)
		self.assertRaises(NotImplementedError, sampler.get_samples, 1)

	def test_sample_handler(self):
		samplers = [Sampler(['name'], lambda x: 0, lambda x: True, {'constant1': 1}), Sampler(['name'], lambda x: 1, lambda x: True, {'constant1': 1})]
		samplers[0].get_samples = lambda x: [samplers[0].make_sample([0])]*x
		samplers[1].get_samples = lambda x: [samplers[1].make_sample([1])]*x
		sampler_set = SamplerSet(samplers)
		samples = sampler_set.get_samples([5, 9])
		self.assertEqual(map(len, samples), [5, 9])
		self.assertEqual(map(lambda x: x.get_metric(), samples[0]), [0]*5)
		self.assertEqual(map(lambda x: x.get_metric(), samples[1]), [1]*9)

	def test_gaussian_get_samples(self):
		sampler = GaussianSampler(['a', 'b'], lambda x: sum(x.values()), lambda x: True, {'constant1': 1}, [1.1, 2], [1, 1])
		samples = sampler.get_samples(10)
		self.assertEqual(len(samples), 10)
		for sample in samples:
			self.assertEqual(sample.attributes.keys(), ['a', 'b', 'constant1'])
			self.assertEqual(sample.attributes['constant1'], 1)

	def test_kde_get_samples(self):
		data = {'a' : [1, 2, 3], 'b': [1, 1.1, 1.2]}
		sampler = KdeSampler(['a', 'b'], lambda x: sum(x.values()), lambda x: True, {'constant1': 1}, data)
		samples = sampler.get_samples(10)
		self.assertEqual(len(samples), 10)
		for sample in samples:
			self.assertEqual(sample.attributes.keys(), ['a', 'b', 'constant1'])
			self.assertEqual(sample.attributes['constant1'], 1)

	def test_kde_constant_with_data(self):
		data = {'a' : [1, 2, 3], 'b': [1, 1.1, 1.2], 'constant1': [1, 2]}
		sampler = KdeSampler(['a', 'b'], lambda x: sum(x.values()), lambda x: True, {'constant1': 1}, data)
		samples = sampler.get_samples(10)
		for sample in samples:
			self.assertEqual(sample.attributes['constant1'], 1)

	def test_tool_get_samples(self):
		noise_model = GaussianNoiseModel([0.01, 0.1])
		scipt_path = "tests/test.sh"
		sampler = ToolSampler(['a', 'b'], lambda x: sum(x.values()), lambda x: True, noise_model, {'constant1': 1}, 'tests/params.tmp', 'tests/samples.tmp', scipt_path, [1, 2])
		samples = sampler.get_samples(10)
		self.assertEqual(len(samples), 10)
		for index, sample in enumerate(samples):
			self.assertEqual(sample.attributes.values(), [index, index, 1])

if __name__ == "__main__":
	unittest.main()