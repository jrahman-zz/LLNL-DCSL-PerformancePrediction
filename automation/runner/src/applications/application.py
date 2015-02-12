
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class Application():

    def __init__(self, start_cores, run_cores):
        self._run_cores = run_cores
        self._start_cores = start_cores

        self._application_dir = ""
        self._load_args = []
        self._start_args = []
        self._run_args = []
        self._stop_args = []
        self._cleanup_args = []

    def load(self):
        """ Load data ahead of any potential benchmark run """
        cmd = ["%s/load.sh" % (self._application_dir)]
        cmd = cmd + self._load_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)


    def interfere(self):
        # TODO, add interference mode

    # TODO, improve to use the with ... as ... idiom

    def start(self):
        """ Start and run the actual benchmark """
        cmd = ["%s/start.sh" % (self._application_dir)]
        cmd = cmd + self._start_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    def run(self):
        """ Run the actual benchmark which generates parseable outputs """
        cmd = ["%s/run.sh" % (self._application_dir)]
        cmd = cmd + self._run_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        features = self._process_output(output)
        return features

    def stop(self):
        """ Stop and benchmark background operations """
        cmd = ["%s/stop.sh" % (self._application_dir)]
        cmd = cmd + self._stop_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    def cleanup(self):
        """ Perform any final cleanup needed """
        cmd = ["%s/cleanup.sh" % (self._appliation_dir)]
        cmd = cmd + self._cleanup_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    def _process_output(self, output):
        """ Process the textual output from the run.sh script """
        pass
