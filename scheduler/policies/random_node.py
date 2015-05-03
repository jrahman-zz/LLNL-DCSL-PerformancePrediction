from scheduler_policy import SchedulerPolicy
import gevent

class RandomNode(SchedulerPolicy):

	def __init__(self):
		SchedulerPolicy.__init__(self)

		# Hostname keyed dict
		self._workers = {}
		
		# Datetime keyed dict of jobs
		self._queue = []
	
		# Id keyed dict of jobs
		self._jobs = {}
		
	
	def _update_workers(self, worker):
		hostname = worker['hostname']
		self._workers[hostname] = worker

	def _queue_jobs(self, jobs):
		for job in jobs:
			self._queue.append(job)
			self._jobs[job['id']] = job
		

	def _update_job(self, id, job):
		self._jobs[id] = job

	def _scheduling_pass(self):
		passed_over = []
		matched = True
		assignments = []
		# Perform a single round of matching
		for job in self._queue:
			cores = job['cores']
			memory = job['memory']
			hosts = [host for host in self._workers.values() if host['free_cores'] < cores and host['free_memory'] < memory]
			logging.info('Scheduler: Found %d possible workers for job %d', len(hosts), job['id'])
			if len(hosts) != 0:
				worker = random.choice(hosts)
				worker['free_memory'] = worker['free_memory'] - memory
				worker['free_processors'] = worker['free_processors'] - cores
				logging.info('Scheduler: Assigned job %s to worker %s', job['id'], worker['hostname'])
				assignments.append((worker, job))
			else:
				logging.info('Scheduler: Failed to find assignment for job %d', job['id'])
				passed_over.append(job)
		
		self._queue = passed_over

	def _get_status(self):
		pass

	def _send_assignments(self, assignments):
		logging.info('Scheduler: Sending %d assignments out to workers...', len(assignments))
		outbound = [gevent.spawn(helpers.start_job, worker['hostname'], job['id'], job['type'], job['cores'], job['size']) for (worker, job) in assignments]
		gvent.join(outbound)
		logging.info('Scheduler: Sent %d assignments out to workers', len(assignments))

	def _lookup_job(self, id):
		if id in self._jobs:
			return self._jobs[id]
		return None

	def _validate_job(self, job):
		""" Validate if an incoming job submission is correct """
		pass
