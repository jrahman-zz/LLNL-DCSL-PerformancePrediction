from benchmarks.stream import StreamCopy, StreamAdd, StreamScale, StreamTriad
from benchmarks.memory import MemoryStream1K, MemoryStream1M, MemoryStream1G
from benchmarks.memory import MemoryRandom1K, MemoryRandom1M, MemoryRandom1G
from benchmarks.iobench import IOBenchRead1M, IOBenchRead4M, IOBenchRead1G
from benchmarks.iobench import IOBenchWrite1M, IOBenchWrite4M, IOBenchWrite1G
from benchmarks.metadata import Metadata

def stream_suite():
    cores = [0, 2]
    bmarks = [StreamCopy(cores), StreamAdd(cores), StreamScale(cores), StreamTriad(cores)]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def memory_stream_suite():
    cores = [1, 3]
    bmarks = [MemoryStream1K(cores), MemoryStream1M(cores), MemoryStream1G(cores)]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def memory_random_suite():
    cores = [0, 2]
    bmarks = [MemoryRandom1K(cores), MemoryRandom1M(cores), MemoryRandom1G(cores)]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def iobench_read_suite():
    cores = [0, 2]
    bmarks = [
            IOBenchRead1M('/tmp/iobench.file', cores),
            IOBenchRead4M('/tmp/iobench.file', cores),
            IOBenchRead1G('/tmp/iobench.file', cores)]

    for bmark in bmarks:
        bmark.start()
    
    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def iobench_write_suite():
    cores = [0, 2]
    bmarks = [
            IOBenchWrite1M('/tmp/iobench.file', cores),
            IOBenchWrite4M('/tmp/iobench.file', cores),
            IOBenchWrite1G('/tmp/iobench.file', cores)]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def metadata_suite():
    cores = [0, 2]
    bmarks = [Metadata('test')]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def main():
    metadata_suite()


if __name__ == '__main__':
    main()
