
from application import Application, Server, Client

class Cassandra(Application):

    def __init__(self, cassandra_dir, ycsb_dir, app_cores, client_cores):
        Application.__init__(self, app_cores, client_cores)
        self._cassandra_dir = cassandra_dir
        self._ycsb_dir = ycsb_dir

class CassandraServer(Server):

    def __init__(self, cassandra_dir, ycsb_dir, cores):
        Server.__init__(self, cores)
        self._cassandra_dir = cassandra_dir
        self._ycsb_dir = ycsb_dir


class CassandraClient(Client):

    def __init__(self, cassandra_dir, ycsb_dir, cores):
        Client.__init__(self, cassandra_dir, ycsb_dir, cores)
        self._cassandra_dir = cassandra_dir
        self._ycsb_dir = ycsb_dir
        
