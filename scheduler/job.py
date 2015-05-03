
class JobState:
	Loading, Running, Waiting, Completed, Failed = range(5)

class Job(object):
	"""
	Represents a job to run on a node
	"""

	def __init__(self, application, cores, memory, hostname):
		self.application = application
		self.cores = cores
		self.memory = memory

#		self.predicted_end = None
		self.start_time = None
		self.finish_time = None
		self.hostname = None
		
		self.status = JobState.Waiting

