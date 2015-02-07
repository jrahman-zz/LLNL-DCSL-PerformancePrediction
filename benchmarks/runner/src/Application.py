
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class Application():

    def __init__(self, server_cores, client_cores):
        self._server_cores = server_cores
        self._client_cores = client_cores

    def start_server(self):
        pass

    def run_client(self):
        pass

    def stop_server(self):
        pass

class Server(greenlet.Greenlet):

    def __init__(self):
        Greenlet.__init__(self)
        pass


class Client(Greenlet):

    def __init__(self):
        Greenlet.__init__(self)
        pass
