
import gevent.greenlet as greenlet
import gevent.subprocess as subprocess

class Application():

    def __init__(self, environ, application_name, start_cores, run_cores):
        
        # Basic information for an application module
        self._application_name = application_name
        self._script_dir = environ['applications'][self._application_name]['script_dir']
        self._application_dir = environ['applications'][self._application_name]['application_dir']
        self._data_dir = environ['data_dir']

        self._interface_args = [self._application_dir, self._data_dir]

        # TODO, clarify how this works
        self._run_cores = run_cores
        self._start_cores = start_cores
        
        self._loaded = False
        self._started = False
        
        self._load_args = []
        self._start_args = []
        self._run_args = []
        self._stop_args = []
        self._cleanup_args = []
        self._interfere_args = []

    def load(self):
        """ Load data ahead of any potential benchmark run """
        cmd = ["%s/load.sh" % (self._script_dir)]
        cmd = cmd + self._interface_args
        cmd = cmd + self._load_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self._loaded = True

    # TODO, improve to use the with ... as ... idiom

    def start(self):
        """ Start and run the actual benchmark """
        if self._started or not self._loaded:
            # TODO, raise error here
            pass

        cores = ','.join(map(lambda x: str(x), self._start_cores))
        cmd = ['taskset', '-c', cores]
        cmd = cmd + ["%s/start.sh" % (self._script_dir)]
        cmd = cmd + self._interface_args
        cmd = cmd + self._start_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self._started = True

    def interfere(self):
        if not self._started or not self._loaded:
            # TODO, raise error here
            pass

        # Create list of allowable cores
        cores = ','.join(map(lambda x: str(x), self._run_cores))

        # Build the command
        cmd = ['taskset', '-c', cores]
        cmd = cmd + ['%s/run.sh' % (self._script_dir)]
        cmd = cmd + self._interface_args
        cmd = cmd + self._interfere_args

        # TODO, implement thisi
        # TODO, run in interruptable loop

    def run(self): 
        """ Run the actual app which generates parseable output """
        if not self._started or not self._loaded:
            # TODO, raise error here
            pass
        # Create list of cores we are allowed to run on
        cores = ','.join(map(lambda x: str(x), self._run_cores))

        # Build our command as required
        cmd = ['taskset', '-c', cores]
        cmd = cmd + ["%s/run.sh" % (self._script_dir)]
        cmd = cmd + self._interface_args
        cmd = cmd + self._run_args

        # Run the command and process the output as neeed
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        features = self._process_output(output)
        return features

    def stop(self):
        """ Stop any benchmark background operations """
        if not self._started:
            # TODO, raise error here
            pass

        cmd = ["%s/stop.sh" % (self._script_dir)]
        cmd = cmd + self._interface_args
        cmd = cmd + self._stop_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self._started = False

    def cleanup(self):
        """ Perform any final cleanup needed """
        if self._loaded = False:
            # TODO, raise error here
            pass

        cmd = ["%s/cleanup.sh" % (self._script_dir)]
        cmd = cmd + self._interface_args
        cmd = cmd + self._cleanup_args
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        self._loaded = False

    def _process_output(self, output):
        pass

 
