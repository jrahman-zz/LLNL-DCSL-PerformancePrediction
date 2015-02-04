
import re
from program import Program
from interference import InterferenceThread

class IOBenchmark(Program):

    def __init__(self, read=True, seconds=5, size='1K', cores=[0]):
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
        self._params = ['-classpath', 'iobench.jar', 'Main', 'run', '-h=20', '/tmp/iobench.file', str(self._seconds), self._runstring]
        self._name = 'iobench_%s_%s' % (self._operation, self._size)

    def _setup(self):
        pass

    def _teardown(self):
        pass

    def _process_output(self, output):
        regex = r"Total for \[%s,%s,%s\]: \d+\.\d+ events \(\d+\.\d+ errors\), mean (\d*\.\d*)ms, 10th (\d*\.\d*)ms, 50th (\d*\.\d*)ms, 90th (\d*\.\d*)ms, 99th (\d*\.\d*)ms, 999th \d*\.\d*ms, 9999th \d*\.\d*ms, min (\d*\.\d*)ms, max (\d*\.\d*)ms$"
        regex = regex % (self._operation.lower(), self._size, self._size)
        result = re.search(regex, output)
        if result == None:
            raise Exception('No match')

        features = {
                'mean': float(result.group(1)),
                '10th': float(result.group(2)),
                '50th': float(result.group(3)),
                '90th': float(result.group(4)),
                '99th': float(result.group(5)),
                'min': float(result.group(6)),
                'max': float(result.group(7))
            }
        return features

class IOBenchInterfere(InterferenceThread):

    def __init__(self, read=True, seconds=30, size='1K', cores=[0]):
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
        self._params = ['-classpath', 'iobench.jar', 'Main', 'run', '-h=20', '/tmp/iobench.file', str(self._seconds), self._runstring]

class IOBenchRead1K(IOBenchmark):
    def __init__(self, cores=[0]):
        IOBenchmark.__init__(self, 5, True, '1K', cores)

class IOBenchInterfereRead1K(IOBenchInterfere):
    def __init__(self, cores=[0]):
        IOBenchInterfere.__init__(self, 30, True, '1K', cores)

class IOBenchRead1M(IOBenchmark):
    def __init__(self, cores=[0]):
        IOBenchmark.__init__(self, 10, True, '1M', cores)

class IOBenchInterfereRead1M(IOBenchInterfere):
    def __init__(self, cores=[0]):
        IOBenchInterfere.__init__(self, 30, True, '1M', cores)

class IOBenchRead1G(IOBenchmark):
    def __init__(self, cores=[0]):
        IOBenchmark.__init__(self, 20, True, '1G', cores)

class IOBenchInterfereRead1G(IOBenchInterfere):
    def __init__(self, cores=[0]):
        IOBenchInterfere.__init__(self, 30, True, '1G', cores)

class IOBenchWrite1K(IOBenchmark):
    def __init__(self, cores=[0]):
        IOBenchmark.__init__(self, 5, False, '1K', cores)

class IOBenchInterfereWrite1K(IOBenchInterfere):
    def __init__(self, cores=[0]):
        IOBenchInterfere.__init__(self, 30, False, '1K', cores)

class IOBenchWrite1M(IOBenchmark):
    def __init__(self, cores=[0]):
        IOBenchmark.__init__(self, 10, False, '1M', cores)

class IOBenchInterfereWrite1M(IOBenchInterfere):
    def __init__(self, cores=[0]):
        IOBenchInterfere.__init__(self, 30, False, '1M', cores)

class IOBenchWrite1G(IOBenchmark):
    def __init__(self, cores=[0]):
        IOBenchmark.__init__(self, 20, False, '1G', cores)

class IOBenchInterfereWrite1G(IOBenchInterfere):
    def __init__(self, cores=[0]):
        IOBenchInterfere.__init__(self, 30, False, '1G', cores)

if __name__ == '__main__':

    test = """Histogram 10 for [write,1M,1M]: 1.0 events (0.0 errors), mean 71.0ms, 10th 71.0ms, 50th 71.0ms, 90th 71.0ms, 99th 71.0ms, 999th 71.0ms, 9999th 71.0ms, min 71.0ms, max 71.0ms
Total for [write,1M,1M]: 173.0 events (0.0 errors), mean 29.8ms, 10th 5.4ms, 50th 20.8ms, 90th 62.9ms, 99th 207ms, 999th 217ms, 9999th 217ms, min 4.63ms, max 217ms"""

    m = IOBenchWrite1M()
    result = m._process_output(test)
    print result
