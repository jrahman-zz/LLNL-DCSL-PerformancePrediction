
from benchmark import Benchmark
from interference import Interference

from glob import glob
from gevent import subprocess
import re

class Metadata(Benchmark):

    def __init__(self, environ, instance=1, cores=[0]):
        Benchmark.__init__(self, environ, cores)
        self._data_dir = '%s/metadata.%s' % (self._data_dir, instance)
        self._cmd = self._benchmark_dir + '/metadata'
        self._params = [self._data_dir, '100'];
        self._name = 'metadata'

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):

        regex = r"Final times, total: \d*\.\d*, median: (\d*\.\d*), mean: \d*\.\d*, p90: (\d*\.\d*)$"
        result = re.search(regex, output)
        if result == None:
            raise Exception('No match found')
        features = {
            'median': float(result.group(1)),
            'p90': float(result.group(2))
        }
        return features

class MetadataInterfere(Interference):

    def __init__(self, environ, cores=[0], nice=0, instance=1):
        Interference.__init__(self, environ, cores, nice)
        self._dir = '%s/metadata.%d' % (environ['data_dir'], instance)
        self._params = [self._dir, '1000'];
        self._cmd = self._benchmark_dir + '/metadata'
        self._name = 'metadata'

    def _teardown(self):
        """ We need to scrub the directory if we were signalled """
        globs = glob(self._dir + '/*')
        subprocess.check_call(['rm', '-f'] + globs)

if __name__ == "__main__":

    test = """Time metadata: 0.117200187
Time metadata: 0.111712514
Time metadata: 0.110697038
Final times, total: 130.639, median: 0.126953, mean: 0.130639, p90: 0.293706"""

    m = Metadata({'benchmark_dir': ''}, 'this/is/a/test')
    result = m._process_output(test)
    print result

    if result['median'] != 0.126953:
        print "Failed to parse the median"
        exit(1)

    if result['p90'] != 0.293706:
        print "Failed to parse the p90 value"
        exit(1)

    exit(0)

