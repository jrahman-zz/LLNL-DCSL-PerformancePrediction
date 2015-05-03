from automation.load_applications import load_applications
from job import JobState

import logging
from datetime import datetime
import gevent
from gevent.subprocess import CalledProcessError

class JobManager(object):
	def __init__(self, environ):
		
		self._environ = environ	
	
		# Callback when a job completes
		self._completion_cb = None
		self._cb_args = None
		self._cb_kwargs = None
		
		# Application object keyed by job id
		self._jobs = {}

		# Application class list keyed by name
		self._applications = load_applications(environ)

		# Dict of running application objects keyed by job ID
		self._running = {}
		self._greenlets = {}
		self._running_info = {}

	def start_job(self, info):
		job_id = info['id']		
		self._greenlets['id'] = greenlet.spawn(JobManager._run_job, self, info)
		return 200

	def get_running_jobs(self):
		""" Get a list of running job ids """
		jobs = [id for id, info in self._running_info.items() if info['status'] == JobState.Running]
		return jobs
		
	def _update_state(self, id, status, start_time=None, finish_time=None, exitcode=None, output=None):
		""" Update the master of the status of a currently running job """
		self._running_info[id]['status'] = status

		if self._running_info[id]['start_time'] is None:
			self._running_info[id]['start_time'] = start_time

		if self._running_info[id]['finish_time'] is None:
			self._running_info[id]['finish_time'] = finish_time

		if output is not None:
			self._running_info[id]['output'] = output
	
		if exitcode is not None:
			self._running_info[id]['exitcode'] = exitcode

		target_host = self._environ['master']
		helper.update_job(target_host, self._running_info[id])

	def _init_job(self, info):
		self._running_info[id] = info
		self._running_info[id]['start_time'] = None
		self._running_info[id]['finish_time'] = None
		self._running_info[id]['exitcode'] = None
		self._running_info[id]['output'] = None
		self._running_info[id]['hostname'] = os.getenv('HOSTNAME')

	def _run_job(self, info):	
		
		try:
			job_id = info['id']
			job_type = info['type']
			cores = info['cores']
			size = info['size']
		except KeyError as k:
			raise ValueError('Missing key in job info')

		app = self._applications[job_type](environ, cores, 2, int(job_id), 0, job_id, size)
		self._running[job_id] = app
		self._init_job(info)	
	
		self._update_status(job_id, JobState.Loading)
		try:
			logging.info('Worker: Loading job %d', int(job_id))
			app.load()
			app.start()
			logging.info('Worker: Loaded job %d', int(job_id))

			self._update_status(job_id, JobState.Running, start_time=datetime.utcnow())
			logging.info('Worker: Starting job %d', int(job_id))
			app.run()
			logging.info('Worker: Finished job %d', int(job_id))
			self._update_status(job_id, JobState.Completed, exitcode=0, finish_time=datetime.utcnow())
		except CalledProcessError as e:
			self._update_status(job_id, JobState.Failed, output=e.output, exitcode=e.returncode, finish_time=datetime.utcnow())
		except Exception as e:
			self._update_status(job_id, JobState.Failed, exitcode=1, finish_time=datetime.utcnow())
		finally:
			logging.info('Worker: Cleaning up job %d', int(job_id))
			app.stop()
			app.cleanup()
			logging.info('Worker: Cleaned up job %d', int(job_id))	
		
		# Perform final operations based on the termination of the job
		try:
			self._job_completed(job_id)
		except Exception as e:
			logging.exception('Worker: Failed to run completion callback for job %d', int(job_id))
		

	def register_completion_cb(self, cb, *args, **kwargs):
		""" Register a given callback function to fire when a job completes """
		self._cb_args = args
		self._cb_kwargs = kwargs
		self._cb = cb

	def _fire_completion_cb(self, job_type, job_id, start_time, finish_time, exitcode):
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

	def _job_completed(self, id):
		info = self._running_info[id]
		self._fire_completion_cb(info['type'], info['id'], info['start_time'], info['finish_time'], info['exitcode'])

