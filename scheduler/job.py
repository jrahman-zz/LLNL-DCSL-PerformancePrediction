
class JobState:
	Running, Waiting, Completed, Failed = range(4)

class Job(object):
	"""
	Represents a job to run on a node
	"""

	def __init__(self, application, cores, memory):
		self.application = application
		self.cores = cores
		self.memory = memory

		self.predicted_end = None
		self.start_time = None
		self.end_time = None
		self.hostname = None
		
		self.state = JobState.Waiting

