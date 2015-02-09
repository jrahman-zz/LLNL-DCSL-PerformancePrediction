
import re
from program import Program
from interference import InterferenceThread

class IOBenchmark(Program):
    """ Base class for IOBench benchmarks """

    def __init__(self, seconds=5, read=True, size='1K', path='/tmp/iobench.file', cores=[0]):
        Program.__init__(self, cores)
        self._read = read
        if read:
            self._operation = 'read'
        else:
            self._operation = 'write'
        self._size = size
        self._seconds = seconds
        self._cmd = 'java'
        self._runstring = ','.join([self._operation, '1', self._size, self._size])
        self._params = ['-classpath', 'iobench.jar', 'Main', 'run', '-h=20', path, str(self._seconds), self._runstring]
        self._name = 'iobench_%s_%s' % (self._operation, self._size)

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        regex = r"Total for \[%s,%s,%s\]: \d+\.\d+ events \(\d+\.\d+ errors\), mean (\d*\.\d*)ms, 10th (\d*\.\d*)ms, 50th (\d*\.\d*)ms, 90th (\d*\.\d*)ms, 99th (\d*(?:\.\d*){0,1})ms, 999th (?:\d*(?:\.\d*){0,1})ms, 9999th (?:\d*(?:\.\d*){0,1})ms, min (\d*\.\d*)ms, max (\d*(?:\.\d*){0,1})ms$"
        regex = regex % (self._operation.lower(), self._size, self._size)
        result = re.search(regex, output)
        if result == None:
            raise Exception('No match')

        features = {
                'mean': float(result.group(1)),
                #'p10': float(result.group(2)),
                'p50': float(result.group(3)),
                'p90': float(result.group(4)),
                #'p99': float(result.group(5)),
                #'min': float(result.group(6)),
                #'max': float(result.group(7))
            }
        return features

class IOBenchInterfere(InterferenceThread):
    """ Base class for IOBench interference threads"""

    def __init__(self, seconds=30, read=True, size='1K', path='/tmp/iobench.file', cores=[0]):
        InterferenceThread.__init__(self, cores)
        self._size = size
        self._seconds = seconds
        self._read = read
        if self._read:
            self._operation = 'read'
        else:
            self._operation = 'write'
        self._name = 'iobench_%s_%s' % (self._operation, self._size)
        self._cmd = 'java'
        self._runstring = ','.join([self._operation, '1', self._size, self._size])
        self._params = ['-classpath', 'iobench.jar', 'Main', 'run', '-h=20', path, str(self._seconds), self._runstring]

class IOBenchRead1M(IOBenchmark):
    def __init__(self, path, cores=[0]):
        IOBenchmark.__init__(self, 10, True, '1M', path, cores)

class IOBenchRead1MInterfere(IOBenchInterfere):
    def __init__(self, path, cores=[0]):
        IOBenchInterfere.__init__(self, 60, True, '1M', path, cores)

class IOBenchRead4M(IOBenchmark):
    def __init__(self, path, cores=[0]):
        IOBenchmark.__init__(self, 15, True, '4M', path, cores)

class IOBenchRead1MInterfere(IOBenchInterfere):
    def __init__(self, path, cores=[0]):
        IOBenchInterfere.__init__(self, 60, True, '4M', path, cores)

class IOBenchRead1G(IOBenchmark):
    def __init__(self, path, cores=[0]):
        IOBenchmark.__init__(self, 20, True, '1G', path, cores)

class IOBenchRead1GInterfere(IOBenchInterfere):
    def __init__(self, path, cores=[0]):
        IOBenchInterfere.__init__(self, 60, True, '1G', path, cores)

class IOBenchWrite1M(IOBenchmark):
    def __init__(self, path, cores=[0]):
        IOBenchmark.__init__(self, 10, False, '1M', path, cores)

class IOBenchWrite1MInterfere(IOBenchInterfere):
    def __init__(self, path, cores=[0]):
        IOBenchInterfere.__init__(self, 60, False, '1M', path, cores)

class IOBenchWrite4M(IOBenchmark):
    def __init__(self, path, cores=[0]):
        IOBenchmark.__init__(self, 15, False, '4M', path, cores)

class IOBenchWrite4MInterfre(IOBenchInterfere):
    def __init__(self, path, cores=[0]):
        IOBenchInterfere.__init__(self, 60, False, '4M', path, cores)

class IOBenchWrite1G(IOBenchmark):
    def __init__(self, path, cores=[0]):
        IOBenchmark.__init__(self, 20, False, '1G', path, cores)

class IOBenchWrite1GInterfere(IOBenchInterfere):
    def __init__(self, path, cores=[0]):
        IOBenchInterfere.__init__(self, 60, False, '1G', path, cores)

if __name__ == '__main__':

    test = """Histogram 10 for [write,1M,1M]: 1.0 events (0.0 errors), mean 71.0ms, 10th 71.0ms, 50th 71.0ms, 90th 71.0ms, 99th 71.0ms, 999th 71.0ms, 9999th 71.0ms, min 71.0ms, max 71.0ms
Total for [write,1M,1M]: 173.0 events (0.0 errors), mean 29.8ms, 10th 5.4ms, 50th 20.8ms, 90th 62.9ms, 99th 207ms, 999th 217ms, 9999th 217ms, min 4.63ms, max 217ms"""

    m = IOBenchWrite1M('/tmp/iobench.file')
    result = m._process_output(test)
    print result
