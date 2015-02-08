from stream import StreamCopy, StreamAdd, StreamScale, StreamTriad
from memory import MemoryStream1K, MemoryStream1M, MemoryStream1G
from memory import MemoryRandom1K, MemoryRandom1M, MemoryRandom1G


def stream_suite():
    cores = [0, 2]
    bmarks = [StreamCopy(cores), StreamAdd(cores), StreamScale(cores), StreamTriad(cores)]

    # Kick off greenlets
    for bmark in bmarks:
        bmark.start()

    # Join back in
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
