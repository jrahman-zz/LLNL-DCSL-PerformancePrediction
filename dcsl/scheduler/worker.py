


class Worker(object):
	"""
	Represent a given worker node
	"""
	def __init__(self, hostname, cores, memory, free_cores, free_memory):
		self._hostname = hostname
		self._free_cores = free_cores
		self._free_memory = free_memory

	def to_json(self):
		return {
			'hostname': self._hostname,
			'cores': self._cores,
			'memory': self._memory
		}

