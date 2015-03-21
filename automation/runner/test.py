from load_environ import load_environ
from load_applications import load_applications
from load_benchmarks import load_benchmarks
from load_interference import load_interference

import gevent

import contexter 

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
        print bmark.run()

def memory_stream_suite(environ, bmark_cls):
    cores = [1, 3]
    bmarks = [
                bmark_cls['MemoryStream1K'](environ, cores),
                bmark_cls['MemoryStream1M'](environ, cores),
                bmark_cls['MemoryStream1G'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.run()

def memory_random_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [
                bmark_cls['MemoryRandom1K'](environ, cores),
                bmark_cls['MemoryRandom1M'](environ, cores),
                bmark_cls['MemoryRandom1G'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.run()

def iobench_read_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [
                bmark_cls['IOBenchRead1M'](environ, cores),
                bmark_cls['IOBenchRead4M'](environ, cores),
                bmark_cls['IOBenchRead128M'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.run()
    

def iobench_write_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [
                bmark_cls['IOBenchWrite1M'](environ, cores),
                bmark_cls['IOBenchWrite4M'](environ, cores),
                bmark_cls['IOBenchWrite128M'](environ, cores)
            ]

    for bmark in bmarks:
        bmark.run()

def metadata_suite(environ, bmark_cls):
    cores = [0, 2]
    bmarks = [bmark_cls['Metadata'](environ, cores)]

    for bmark in bmarks:
        bmark.run()

def main():
    modules = ['applications.json', 'benchmarks.json', 'interference.json']
    environ = load_environ('config.json', modules)

    apps = load_applications(environ)
    print apps
    bmarks = load_benchmarks(environ)
    threads = load_interference(environ)

    #bmark1 = bmarks['IOBenchV2Read1M'](environ, [1, 2], 1)
    #bmark2 = bmarks['IOBenchV2Write4M'](environ, [1, 2], 2)
    #bmark1.run()
    #bmark2.run()
    #bmark = bmarks['Whetstone'](environ, [1, 2], 2)
    #print bmark.run()
    #bmark = bmarks['Linpack'](environ, [1, 2], 2)
    #print bmark.run()
    bmark = bmarks['Stream'](environ, [1, 2], 2)
    print bmark.run()

    #interference1 = threads['Metadata'](environ, [1, 2], [1], -5, 1)
    interference2 = threads['IOBenchV2Read1M'](environ, [2], [1], 10, 2)
    interference3 = threads['IOBenchV2Write4M'](environ, [1], [1], 10, 1)

    interference = [interference2, interference3]
    with contexter.ExitStack() as top_stack:
        for thread in interference:
            top_stack.enter_context(thread)
        with contexter.ExitStack() as stack:
            for thread in interference:
                stack.enter_context(thread.interfere())
            print('Starting to sleep...')
            gevent.sleep(10)
            print('Woke up')
    

    app = apps['SpecSoplex'](environ, [0, 1], [2, 3])
    
    app.load()
    app.start()
    print(app.run())
    app.stop()
    app.cleanup()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
