
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class InterferenceThread(greenlet.Greenlet):

    def __init__(self, cores=[0]):
        Greenlet.__init__(self)
        self._cores = cores
        self._process = None
        self._keep_running = True

    def __str__(self):
        return self._name

    def kill(self):
        self._stop()
        super(InterferenceThread, self).kill()

    def join(self):
        self._stop()
        super(InterferenceThread, self).join()

    def _stop(self):
        if self._process is not None:
            self._process.kill()
        else:
            self._keep_running = False
        self._process = None


    def _run(self):
        cores = ','.join(map(cores, lambda x: str(x)))
        args = ['taskset', '-c', cores, self._cmd] + self._params
        while self._keep_running:
            self._process = subprocess.Popen(args)
            return_code = self._process.wait()
            if not return_code == 0:
                self._keep_running = False
                raise Exception('Process failure')

