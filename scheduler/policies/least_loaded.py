
from scheduler_policy import SchedulerPolicy

class LeastLoaded(SchedulerPolicy):

	def __init__(self):
		SchedulerPolicy.__init__(self)

		self._waiting_job_queue = []
		self._job_dict = {}

		self._worker_nodes = []


	def _update_workers(self, worker):
		pass


	def _update_measurements(self, measurements):
		pass

	def _update_job(self, id, job_info):
		pass

	def _queue_jobs(self, jobs):
		for job in jobs:
			self._insert_job(job)
		

	def _scheduling_pass(self):
		
	
	def _insert_job(self, job):
		logging.info('Queuing job: %s', str(job))
		job['hostname'] = None
		job['start_time'] = None
		job['end_time'] = None
		job['state'] = JobState.Waiting
		if 'cores' not in job:
			raise ValueError('No core count given')
		
		self._waiting_job_queue.append(job)
		self._job_dict[job['id']] = job

