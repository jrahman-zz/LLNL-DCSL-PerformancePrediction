
from application import Application, ApplicationInterfere

class Cassandra(Application):

    def __init__(self, environ, app_cores, client_cores):
        Application.__init__(self, environ, 'Cassandra', app_cores, client_cores)
        self._pid_file = self._tmp_dir + '/cassandra.pid'
        self._cassandra_include = self._script_dir + '/cassandra.in.sh'
        self._ycsb_dir = environ['application']['params']['ycsb_dir']

        self._run_params = [self._ycsb_dir, 1000000]
        self._load_params = [self._ycsb_dir, self._pid_file, self._cassandra_include]
        self._start_params = [self._pid_file, self._cassandra_include]

    def _parse_output(self, output)
        # TODO
        pass

class CassandraInterfere(ApplicationInterfere):

    def __init__(self, environ, app_cores, client_cores):
        ApplicationInterfere.__init__(self, environ, 'Cassandra', app_cores, client_cores)
        self._pid_file = self._tmp_dir + '/cassandra.pid'
        self._cassandra_include = self._script_dir + '/cassandra.in.sh'

        self._run_prams = [self._ycsb_dir, 10000000]
        self._load_params = [self._ycsb_dir, self._pid, self._cassandra_include]
        self._start_params = [self._pid_file, self._cassandra_include]
