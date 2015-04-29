from automation.runner.load_applications import load_applications

class JobManager(object):


	def __init__(self, environ):
		
		# Track the largest instance for each application type
		self.largest_instance = {}
		
		# Callback when a job completes
		self._completion_cb = None
		self._cb_args = None
		self._cb_kwargs = None
		
		# Application object keyed by job id
		self._jobs = {}

		# Application class list keyed by name
		self._applications = load_applications(environ)

	def start_job(info):
		job_type = info['type']
		cores = info['cores']

	def register_completion_cb(self, cb, *args, **kwargs):
		""" Register a given callback function to fire when a job completes """
		self.
		self._cb_args = args
		self._cb_kwargs = kwargs

	def _fire_completion_cb(self, job_type, job_id, start_time, end_time, exit_code):
		if self._completion_cb is not None:
			if self._cb_args is not None:
				args = self._cb_args
			else:
				args = []
			if self._cb_kwargs is not None:
				kwargs = self._cb_kwargs
			else:
				kwargs = {}
			args.append(job_type)
			args.append(job_id)
			args.append(start_time)
			args.append(end_time)
			args.append(exit_code)
			self._completion_cb(*args, **kwargs)

