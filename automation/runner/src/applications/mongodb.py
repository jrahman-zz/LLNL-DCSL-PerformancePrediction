
from application import Application
from parse_ycsb import parse

class MongoDB(Application):

    def __init__(self, environ, app_cores, client_cores):
        Application.__init__(self, environ, 'MongoDB', app_cores, client_cores)

        # Build params related to the mongodb interface scripts
        self._ycsb_dir = environ['ycsb_dir']

        self._run_params = [self._ycsb_dir, '1000000']
        self._load_params = [self._ycsb_dir]
        self._interfere_params = [self._ycsb_dir, '10000000']

    def _process_output(self, output):
        return parse(output)
