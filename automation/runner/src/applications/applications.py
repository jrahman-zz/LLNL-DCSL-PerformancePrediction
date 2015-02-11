
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class Application():

    def __init__(self, appliation_cores, client_cores):
        self._application_cores = application_cores
        self._client_cores = client_cores
        self._server = None

    def start_server(self):
        self._server = self._server_class(self._application_cores)
        # TODO, finish this

    def run_client(self):
        self._client = self._client_class(self._client_cores)
        self._client.start()
        output = self._client.get()
        pass

    def stop_server(self):
        pass

class Server(greenlet.Greenlet):

    def __init__(self, cores=[0]):
        Greenlet.__init__(self)
        self._cores = cores

    def _run(self):
        pass


class Client(Greenlet):

    def __init__(self, cores=[0]):
        Greenlet.__init__(self)
        self._cores = cores

    def _run(self):
        output = "TODO"
        output = self._parse_output(output)
        return output

    def _parse_output(self, output):
        pass
