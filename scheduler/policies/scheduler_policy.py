
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
		self._update_workers(worker)

	def update_measurements(self, measurements):
		""" Receive updated information about the measurements """
		self._update_measurements(measurements)

	def update_job(self, id, job_info):
		""" Receive updated information about a job completion """
		job = self.lookup_job(id)
		
		now = None
		job['finish_time'] = job_info['finish_time']
		if job_info['status'] == JobState.Completed:
			logging.info('Job %d completed at %s, started at %s', id, job['finish_time'], job['start_time'])
			# TODO, switch state to completed
		else:
			logging.info('Job %d failed at %s, started at %s', id, job['finish_time'], job['start_time'])
			# TODO, switch state to failed
		return self._update_job(self, id, job_info)

	def queue_jobs(self, jobs):
		""" Add a new request for a job """
		# Allocate IDs for each new job	
		for i in range(0, len(jobs)):
			id = self._get_id()
			jobs[i]['id'] = id

		for job in jobs:
			self.validate_job(job)

		return self._queue_jobs(self, jobs)

	def scheduling_pass(self):
		""" Run the scheduling algorithm once """
		self._scheduling_pass()

	def get_status(self):
		""" Return JSON containing status information """
		self._get_status()

	def lookup_job(self, id):
		self._lookup_job(id)

	def validate_job(self, job):
		if 'application' not in job:
			raise ValueError('No application given')
		if 'cores' not in job:
			raise ValueError('No cores given')
		self._validate_job

