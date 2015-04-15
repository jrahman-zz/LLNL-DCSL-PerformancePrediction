from benchmark import Benchmark
from interference import Interference

import re
import logging

class IOBenchmark(Benchmark):
    """ Base class for IOBench benchmarks """

    def __init__(self, environ, cores=[0], seconds=5, read=True, size='1K', instance=1):
        Benchmark.__init__(self, environ, cores)
        self._read = read
        if read:
            self._operation = 'read'
            self._type = self._operation
        else:
            self._operation = 'write100'
            self._type = 'write'
        self._size = size
        self._seconds = seconds
        self._path = '%s/iobench.%d' % (environ['data_dir'], instance)
        self._cmd = 'java'
        self._runstring = ','.join([self._operation, '1', self._size, '1K'])
        self._params = ['-classpath', self._benchmark_dir + '/iobench.jar', 'Main', 'run', '-h=20', self._path, str(self._seconds), self._runstring]
        self._name = 'iobench_%s_%s' % (self._type, self._size)

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        regex = r"Total for \[%s,%s,%s\]: \d+\.\d+ events \(\d+\.\d+ errors\), mean (\d*(?:\.\d*)?)ms, 10th (\d*(?:\.\d*)?)ms, 50th (\d*(?:\.\d*)?)ms, 90th (\d*(?:\.\d*)?)ms, 99th (\d*(?:\.\d*)?)ms, 999th (\d*(?:\.\d*)?)ms, 9999th (\d*(?:\.\d*)?)ms, min (\d*(?:\.\d*)?)ms, max (\d*(?:\.\d*)?)ms$"
        regex = regex % (self._operation, self._size, '1K')
        result = re.search(regex, output)
        if result == None:
            logging.warning('Mismatch: %s', output)
            raise Exception('No match')

        features = {
                'mean': float(result.group(1)),
                #'p10': float(result.group(2)),
                #'p50': float(result.group(3)),
                'p90': float(result.group(4)),
                #'p99': float(result.group(5)),
                #'min': float(result.group(6)),
                #'max': float(result.group(7))
            }
        return features

class IOBenchInterfere(Interference):
    """ Base class for IOBench interference threads"""

    def __init__(self, environ, cores=[0], seconds=30, read=True, size='1K', nice=0, instance=1):
        Interference.__init__(self, environ, cores, nice)
        self._size = size
        self._seconds = seconds
        self._read = read
        if self._read:
            self._operation = 'read'
            self._type = self._operation
        else:
            self._operation = 'write100'
            self._type = 'write'
        self._name = 'iobench_%s_%s' % (self._type, self._size)
        self._path = '%s/iobench.%d' % (environ['data_dir'], instance)
        self._cmd = 'java'
        self._runstring = ','.join([self._operation, '1', self._size, self._size])
        self._params = ['-classpath', self._benchmark_dir + '/iobench.jar', 'Main', 'run', '-h=20', self._path, str(self._seconds), self._runstring]

class IOBenchRead1M(IOBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmark.__init__(self, environ, cores, 10, True, '1M', instance)

class IOBenchRead1MInterfere(IOBenchInterfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchInterfere.__init__(self, environ, cores, 60, True, '1M', nice, instance)

class IOBenchRead4M(IOBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmark.__init__(self, environ, cores, 15, True, '4M', instance)

class IOBenchRead4MInterfere(IOBenchInterfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchInterfere.__init__(self, environ, cores, 60, True, '4M', nice, instance)

class IOBenchRead128M(IOBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmark.__init__(self, environ, cores, 20, True, '128M', instance)

class IOBenchRead128MInterfere(IOBenchInterfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchInterfere.__init__(self, environ, cores, 60, True, '128M', nice, instance)

class IOBenchWrite1M(IOBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmark.__init__(self, environ, cores, 10, False, '1M', instance)

class IOBenchWrite1MInterfere(IOBenchInterfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchInterfere.__init__(self, environ, cores, 60, False, '1M', nice, instance)

class IOBenchWrite4M(IOBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmark.__init__(self, environ, cores, 15, False, '4M', instance)

class IOBenchWrite4MInterfere(IOBenchInterfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchInterfere.__init__(self, environ, cores, 60, False, '4M', nice, instance)

class IOBenchWrite128M(IOBenchmark):
    def __init__(self, environ, cores=[0], instance=1):
        IOBenchmark.__init__(self, environ, cores, 20, False, '128M', instance)

class IOBenchWrite128MInterfere(IOBenchInterfere):
    def __init__(self, environ, cores=[0], extra_cores=[1], nice=0, instance=1):
        IOBenchInterfere.__init__(self, environ, cores, 60, False, '128M', nice, instance)

if __name__ == '__main__':

    test = """Histogram 10 for [write,1M,1M]: 1.0 events (0.0 errors), mean 71.0ms, 10th 71.0ms, 50th 71.0ms, 90th 71.0ms, 99th 71.0ms, 999th 71.0ms, 9999th 71.0ms, min 71.0ms, max 71.0ms
Total for [write,1M,1M]: 173.0 events (0.0 errors), mean 29.8ms, 10th 5.4ms, 50th 20.8ms, 90th 62.9ms, 99th 207ms, 999th 217ms, 9999th 217ms, min 4.63ms, max 217ms"""

    m = IOBenchWrite1M(1)
    result = m._process_output({'benchmark_dir': ''}, test)
    print result
