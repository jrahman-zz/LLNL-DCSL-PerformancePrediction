from benchmark import Benchmark
import re
import logging

class Livermore(Benchmark):

    def __init__(self, environ, cores=[0], instance=1):
        Benchmark.__init__(self, environ, cores)
        self._cmd = self._benchmark_dir + '/lloops'
        self._params = []
        self._name = 'lloops'

    def _process_output(self, output):
        regex = r"Maximum\s*Average\s*Geomean\s*Harmean\s*Minimum\s*\n\s*(\d+(?:\.\d+))\s*(\d+(?:\.\d+))\s*(\d+(?:\.\d+))\s*(\d+(?:\.\d+))\s*(\d+(?:\.\d+))"

        result = re.search(regex, output)
        if result == None:
            logging.error('Mismatch: %s', output)
            raise Exception('No match')
        features = {
                'maximum': float(result.group(1)),
                'average': float(result.group(2)),
                'geomean': float(result.group(3)),
                'harmean': float(result.group(4)),
                'minimum': float(result.group(5))
        }
        return features

if __name__ == "__main__":
    benchmark = Livermore({'benchmark_dir': '../../benchmarks/bin', 'data_dir': ''})
    print benchmark.run()
