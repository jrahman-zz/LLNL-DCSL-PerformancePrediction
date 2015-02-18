from load_environ import load_environ
from load_applications import load_applications
from load_benchmarks import load_benchmarks

import logging

def stream_suite(environ, bmarks_cls):
    cores = [0, 2]
    bmarks = [
                bmark_cls['StreamCopy'](environ, cores),
                bmark_cls['StreamAdd'](environ, cores),
                bmark_cls['StreamScale'](environ, cores),
                bmark_cls['StreamTriad'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def memory_stream_suite(environ, bmark_cls):
    cores = [1, 3]
    bmarks = [
                bmark_cls['MemoryStream1K'](environ, cores),
                bmark_cls['MemoryStream1M'](environ, cores),
                bmark_cls['MemoryStream1G'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def memory_random_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [
                bmark_cls['MemoryRandom1K'](environ, cores),
                bmark_cls['MemoryRandom1M'](environ, cores),
                bmark_cls['MemoryRandom1G'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def iobench_read_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [
                bmark_cls['IOBenchRead1M'](environ, '/tmp/iobench.file', cores),
                bmark_cls['IOBenchRead4M'](environ, '/tmp/iobench.file', cores),
                bmark_cls['IOBenchRead1G'](environ, '/tmp/iobench.file', cores)
            ]

    for bmark in bmarks:
        bmark.start()
    
    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def iobench_write_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [
                bmark_cls['IOBenchWrite1M'](environ, '/tmp/iobench.file', cores),
                bmark_cls['IOBenchWrite4M'](environ, '/tmp/iobench.file', cores),
                bmark_cls['IOBenchWrite1G'](environ, '/tmp/iobench.file', cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def metadata_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [bmark_cls['Metadata'](environ)]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def main():
    environ = load_environ('config.json', ['applications.json', 'benchmarks.json'])
    apps = load_applications(environ)
    (bmarks, inter) = load_benchmarks(environ)

    bmark = bmarks['StreamAdd'](environ, [1, 2])
    bmark.start()
    bmark.join()

    app = apps['MongoDB'](environ, [0, 1], [2, 3])
    
    app.load()
    app.start()
    print app.run()
    app.stop()
    app.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
