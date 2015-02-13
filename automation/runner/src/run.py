from benchmarks.stream import StreamCopy, StreamAdd, StreamScale, StreamTriad
from benchmarks.memory import MemoryStream1K, MemoryStream1M, MemoryStream1G
from benchmarks.memory import MemoryRandom1K, MemoryRandom1M, MemoryRandom1G
from benchmarks.iobench import IOBenchRead1M, IOBenchRead4M, IOBenchRead1G
from benchmarks.iobench import IOBenchWrite1M, IOBenchWrite4M, IOBenchWrite1G
from benchmarks.metadata import Metadata

def stream_suite(environ):
    cores = [0, 2]
    bmarks = [
                StreamCopy(environ, cores),
                StreamAdd(environ, cores),
                StreamScale(environ, cores),
                StreamTriad(environ, cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def memory_stream_suite(environ):
    cores = [1, 3]
    bmarks = [
                MemoryStream1K(environ, cores),
                MemoryStream1M(environ, cores),
                MemoryStream1G(environ, cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def memory_random_suite(environ):
    cores = [0, 2]
    bmarks = [
                MemoryRandom1K(environ, cores),
                MemoryRandom1M(environ, cores),
                MemoryRandom1G(environ, cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def iobench_read_suite(environ):
    cores = [0, 2]
    bmarks = [
                IOBenchRead1M(environ, '/tmp/iobench.file', cores),
                IOBenchRead4M(environ, '/tmp/iobench.file', cores),
                IOBenchRead1G(environ, '/tmp/iobench.file', cores)
            ]

    for bmark in bmarks:
        bmark.start()
    
    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def iobench_write_suite(environ):
    cores = [0, 2]
    bmarks = [
                IOBenchWrite1M(environ, '/tmp/iobench.file', cores),
                IOBenchWrite4M(environ, '/tmp/iobench.file', cores),
                IOBenchWrite1G(environ, '/tmp/iobench.file', cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def metadata_suite(environ):
    cores = [0, 2]
    bmarks = [Metadata(environ, 'test')]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def main():
    environ = {'benchmark_dir': '/home/jprahman/LLNL-DCSL-PerformancePrediction/benchmarks/bin'}
    metadata_suite(environ)
    iobench_read_suite(environ)


if __name__ == '__main__':
    main()
