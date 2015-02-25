from load_environ import load_environ
from load_applications import load_applications
from load_benchmarks import load_benchmarks

import gevent

import argparse
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
                bmark_cls['IOBenchRead1M'](environ, cores),
                bmark_cls['IOBenchRead4M'](environ, cores),
                bmark_cls['IOBenchRead128M'](environ, cores)
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
                bmark_cls['IOBenchWrite1M'](environ, cores),
                bmark_cls['IOBenchWrite4M'](environ, cores),
                bmark_cls['IOBenchWrite128M'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.start()

    for bmark in bmarks:
        bmark.join()

    for bmark in bmarks:
        print bmark.value

def metadata_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [bmark_cls['Metadata'](environ, cores)]

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

    bmark1 = bmarks['IOBenchWrite1M'](environ, [1, 2], 1)
    bmark2 = bmarks['IOBenchWrite4M'](environ, [1, 2], 2)
    #bmark1.start()
    #bmark2.start()
    #bmark1.join()
    #bmark2.join()

    #interference1 = inter['Metadata'](environ, [1, 2], -5, 1)
    #interference2 = inter['StreamAdd'](environ, [2], 10, 2)
    #interference3 = inter['StreamAdd'](environ, [1], 10, 1)
    #interference1.start()
    #interference2.start()
    #interference3.start()
    print 'Starting to sleep...'
    #gevent.sleep(20)
    print 'Woke up'
    #interference1.join()
    #interference2.join()
    #interference3.join()

    app = apps['SpecSoplex'](environ, [0, 1], [2, 3])
    
    app.load()
    app.start()
    print app.run()
    app.stop()
    app.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
