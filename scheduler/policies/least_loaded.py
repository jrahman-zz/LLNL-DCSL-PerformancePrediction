
from scheduler_policy import SchedulerPolicy

class LeastLoaded(SchedulerPolicy):

	def __init__(self):
		SchedulerPolicy.__init__(self)
