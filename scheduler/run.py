

class Run(object):
	"""
	Represent information about a given application run
	"""

	def __init__(self, app_name, runtime):
		self._app_name = app_name
		self._runtime = runtime
