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

import logging
import uuid
import numpy as np

class Sample:
	def __init__(self, attributes, metric, valid):
		self.logger = logging.getLogger('Sample')
		self.attributes = attributes
		self.metric = metric
		self.valid = valid
		self.id = uuid.uuid4()

	def get_metric(self):
		try:
			return self.metric(self.attributes)
		except Exception as err:
			self.logger.error('Metric evaluation failed with exception: ' + str(err))
			raise Exception('Metric evaluation failed', err)

	def is_valid(self):
		try:
			return self.valid(self.attributes)
		except Exception as err:
			self.logger.error('Sample validity check failed with exception: ' + str(err))
			raise Exception('Sample validity check failed', err)

	#def __cmp__(self, other):
	#	if other == None:
	#		return 1 if self.isValid() else -1
	#	
	#	if self.isValid()*self.getMetricValue() < other.isValid()*other.getMetricValue():
	#		return -1
	#	elif self.isValid()*self.getMetricValue() == other.isValid()*other.getMetricValue():
	#		return 0
	#	else:
	#		return 1

	#def __repr__(self):
	#	return str(self.attributes)

	#def __getstate__(self):
	#	d = self.__dict__
	#	d['metric'] = None
	#	d['valid_function'] = None
	#	d['logger'] = None
	#	return d

class NoiseModel(object):
	def add_noise(self, x, count):
		raise NotImplementedError()

class GaussianNoiseModel(NoiseModel):
	def __init__(self, variance):
		self.variance = variance
	def add_noise(self, x, count):
		if len(x) != len(self.variance):
			raise Exception('Dimension mismatch: expected x with dim ' + str(len(self.variance)))
		return np.random.multivariate_normal(x, np.diag(self.variance),count)

