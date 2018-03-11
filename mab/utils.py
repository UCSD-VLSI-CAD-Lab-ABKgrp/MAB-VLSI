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

