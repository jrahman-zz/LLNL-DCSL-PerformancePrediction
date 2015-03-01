from interference import InterferenceThread

class DummyInterfere(InterferenceThread):
    def __init__(self, environ, cores=[0], extra_cores=[1], instance=1):
        InterferenceThread.__init__(self, environ, cores, 0)
        self._cmd = 'sleep'
        self._params = [str(10)]
        self._name = 'dummy'
