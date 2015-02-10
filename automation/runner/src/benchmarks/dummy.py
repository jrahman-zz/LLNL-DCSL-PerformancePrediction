
from interference import InterferenceThread

class DummyInterfere(InterferenceThread):

    def __init__(self, cores=[0]):
        InterferenceThread.__init__(self, cores)
        self._cmd = 'sleep'
        self._params = [str(10)]
        self._name = 'dummy'
