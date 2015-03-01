from interference import Interference

class DummyInterfere(Interference):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        Interference.__init__(self, environ, cores, 0)
        self._cmd = 'sleep'
        self._params = [str(30)]
        self._name = 'dummy'
