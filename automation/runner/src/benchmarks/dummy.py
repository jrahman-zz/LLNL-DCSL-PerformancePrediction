from interference import InterferenceThread

class DummyInterfere(InterferenceThread):
    def __init__(self, environ, cores=[0], instance=1):
        InterferenceThread.__init__(self, environ, cores)
        self._cmd = 'sleep'
        self._params = [str(10)]
        self._name = 'dummy'
