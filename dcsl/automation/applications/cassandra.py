
from application import Application
from parse_ycsb import parse

class Cassandra(Application):

    def __init__(self, environ, app_cores, client_cores, nice=0, instance=1):
        Application.__init__(self, environ, 'Cassandra', app_cores, client_cores, nice, instance)
        
        # Build params related to the cassandra interface scripts
        self._pid_file = self._data_dir + '/cassandra.pid' # TODO, use a better PID file
        self._cassandra_include = self._script_dir + '/cassandra.in.sh'
        self._ycsb_dir = environ['ycsb_dir']

        self._run_params = [self._ycsb_dir, '1000000']
        self._interfere_params = [self._ycsb_dir, '10000000']
        self._load_params = [self._ycsb_dir, self._pid_file, self._cassandra_include]
        self._start_params = [self._pid_file, self._cassandra_include]
        self._stop_params = [self._pid_file]

    def _process_output(self, output):
        return parse(output)

