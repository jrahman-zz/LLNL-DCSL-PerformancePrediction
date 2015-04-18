
import logging

class SchedulerPolicy(object):

	def __init__(self):
		self._next_job_id = 0

	def _get_id(self):
		id = self._next_job_id
		self._next_job_id = self._next_job_id + 1
		return id

	def update_workers(self, worker):
		""" Receive updated information about the worker status  """
		pass

	def update_measurements(self, measurements):
		""" Receive updated information about the measurements """
		pass

	def update_job(self, id, job_info):
		""" Receive updated information about a job completion """
		job = lookup_job(id)
		
		# TODO Find time string
		now = None
		job.finish_time = job_info['finish_time']
		if job_info['status'] == JobState.Completed:
			logging.info('Job %d completed at %s, started at %s', id, job.finish_time, job.start_time)
			# TODO, switch state to completed
		else:
			logging.info('Job %d failed at %s, started at %s', id, job.finish_time, job.start_time)
			# TODO, switch state to failed
		

	def queue_jobs(self, jobs):
		""" Add a new request for a job """
		ids = []
		for i in range(0, len(jobs)):
			id = self._get_id()
			jobs[i].id = id
		self._queue_job(self, jobs)
		
		return jobs

	def scheduling_pass(self):
		""" Run the scheduling algorithm once """
		pass

	def get_status(self):
		""" Return JSON containing status information """
		pass

	def lookup_job(self, id):
		# Implement in subclass
		pass

