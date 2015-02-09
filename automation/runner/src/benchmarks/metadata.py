
from program import Program
from interference import InterferenceThread
import re

class Metadata(Program):

    def __init__(self, path, cores=[0]):
        Program.__init__(self, cores)
        self._cmd = './metadata'
        self._params = [path, '100'];
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

class MetadataInference(InterferenceThread):

    def __init__(self, path, cores=[0]):
        InterferenceThread.__init__(self, cores)
        self._params = [path, '1000'];
        self._cmd = './metadata'
        self._name = 'metadata'


if __name__ == "__main__":

    test = """Time metadata: 0.117200187
Time metadata: 0.111712514
Time metadata: 0.110697038
Final times, total: 130.639, median: 0.126953, mean: 0.130639, p90: 0.293706"""

    m = Metadata('this/is/a/test')
    result = m._process_output(test)
    print result

    if result['median'] != 0.126953:
        print "Failed to parse the median"
        exit(1)

    if result['p90'] != 0.293706:
        print "Failed to parse the p90 value"
        exit(1)

    exit(0)

