import gevent
import logging
from datetime import datetime, timedelta
from automation.load_benchmarks import load_benchmarks


class MeasurementManager:

	def __init__(self, environ):
		self._benchmarks = load_benchmarks(environ)
	
		self._start_time = None
		self._end_time = None
		self._is_benchmarking = None

		self._benchmarks_used = Set()

		# Keyed by name, then a list
		self._latest_measurements = {}
		# Keyed by time, then 
		self._measurements = {}
		
		self._loopdelta

		self._keep_looping = False
		self._looper = None

	def run_benchmarks(self):
		self._is_benchmarking = True
		self._start_time = datetime.utcnow()
		logging.info('Starting benchmarks at %s', self._start_time)

		self._finish_time = datatime.utcnow()
		logging.info('Ending benchmarks at %s', self._end_time)
		pass

	def start_loop(self):
		""" Start benchmarking loop """
		self._keep_looping = True
		self._looper = gevent.spawn(MeasurementManager._loop_main, self)
		self._looper.start()

	def end_loop(self):
		""" End benchmarking loop """
		pass

	def _run_benchmarks(self):
		pass

	def _loop_main(self):
		logging.info('MeasurementManager: Loop main starting')	
		# TODO
		while self._keep_looping:
			gevent.sleep(100)

		logging.info('MeasurementManager: Loop main ending')

	def _insert_measurement(self, key, value, time):
		if key not in self._latest_measurement:
			self._latest_measurement[key] = []
		self._latest_measurements[key].append(value)
		if time not in self._measurements:
			self._measurements[time] = dict()
		self._measurements[time][key] = value
