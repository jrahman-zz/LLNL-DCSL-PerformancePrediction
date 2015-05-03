
# Import all the benchmarks
from benchmarks.stream import StreamCopy, StreamAdd, StreamScale, StreamTriad
from benchmarks.memory import MemoryStream1K, MemoryStream1M, MemoryStream1G
from benchmarks.memory import MemoryRandom1K, MemoryRandom1M, MemoryRandom1G
from benchmarks.iobench import IOBenchRead1M, IOBenchRead4M, IOBenchRead1G
from benchmarks.iobench import IOBenchWrite1M, IOBenchWrite4M, IOBenchWrite1G
from benchmarks.metadata import Metadata

import argparse
import random


def parse_args():

    parser = argparse.ArgumentParser(description='Runner')
    # TODO, add arguments
    parser.add_argument()

def random_partition(bmarks):
    shuffled = bmarks
    random.shuffle(shuffled)
    first = shuffled[0:(len(shuffled)/2)]
    last = shuffled[(len(shuffled)/2:]
    return (first, last)

def run_benchmarks(bmarks, output):
    """ Run a given list of benchmarks, adding the results to the output dictionary """
    for bmark in bmarks:
        bmark.start()
        result = bmark.get() # TODO, error handling here would be nice
        for key in result.keys():
            feature_name = "%s_%s" % (str(bmark).lower(), key.lower())
            if not feature_name in output:
                output[feature_name] = []
            output[feature_name].append(result[key])
    return output

def run_application(application, output):
    """ Run the given application and add appropriate results to output """
    result = application.run() # TODO, finish this interface
    
    # Add columns if they haven't been seen yet
    if not 'application' in output:
        output['application'] = []
    if not 'y' in output:
        output['y'] = []
    
    output['application'].append(str(application).lower())
    output['y'].append(result)
    return output

def print_output(f, output):

    # Print the header first
    keys = output.keys() # Reuse this to ensure keys remain in exact same order
    header_line = ','.join(map(lambda x: x.lower(), keys))
    f.write(header_line + '\n')

    rows = []
    for i in range(0, len(output['y'])):
        output_line = ','.join(map(lambda key: output[key][i], keys))
        f.write(output_line + '\n')

def create_benchmarks(config):
    
    cores = config['cores']
    iotestfile = config['iotestfile']
    iodir = config['iodir']

    stream_bmarks = [
                StreamCopy(cores),
                StreamAdd(cores),
                StreamScale(cores),
                StreamTriad(cores)
            ]
    memory_random_bmarks = [
                MemoryRandom1K(cores),
                MemoryRandom1M(cores),
                MemoryRandom1G(cores)
            ]
    memory_stream_bmarks = [
                MemoryStream1K(cores),
                MemoryStream1M(cores),
                MemoryStream1G(cores)
            ]
    iobench_write_bmarks = [
                IOBenchWrite1M(iotestfile, cores),
                IOBenchWrite4M(iotestfile, cores),
                IOBenchWrite1G(iotestfile, cores)
            ]
    iobench_read_bmarks = [
                IOBenchRead1M(iotestfile, cores),
                IOBenchRead4M(iotestfile, cores),
                IOBenchRead1G(iotestfile, cores
            ]
    metadata_bmarks = [
                Metadata(iodir, cores)
            ]

    # Combine all the bmarks into unified list
    bmarks = stream_bmarks
    bmarks = bmarks + memory_random_bmarks + memory_stream_bmarks
    bmarks = bmarks + iobench_write_bmarks + iobench_read_bmarks
    bmarks = bmarks + metadata_bmarks
    return bmarks

def create_interference_threads(config):
    
    cores = config['cores']
    iodir = config['iodir']
    iotestfile = config['iotestfile']

    # Interference threads
    stream_interfere = [
                StreamCopyInterfere(cores),
                StreamAddInterfere(cores),
                StreamScaleInterfere(cores),
                StreamTriadInterfere(cores)
            ]
    memory_random_interfere = [
                MemoryRandom1KInterfere(cores),
                MemoryRandom1MInterfere(cores),
                MemoryRandom1GInterfere(cores)
            ]
    memory_stream_interfere = [
                MemoryStream1KInterfere(cores),
                MemoryStream1MInterfere(cores),
                MemoryStream1GInterfere(cores)
            ]
    iobench_write_interfere = [
                IOBenchWrite1MIntefere(iotestfile, cores),
                IOBenchWrite4MIntefere(iotestfile, cores),
                IOBenchWrite1GIntefere(iotestfile, cores)
            ]
    iobench_read_interfere = [
                IOBenchRead1MIntefere(iotestfile, cores),
                IOBenchRead4MIntefere(iotestfile, cores),
                IOBenchRead1GIntefere(iotestfile, cores
            ]
    metadata_interfere = [
                MetadataInterfere(iodir, cores)
            ]

    # TODO, add noop interference thread to represent interference free conditions
    interference_threads = stream_interfere
    interference_threads = interferance_threads + memory_random_interfere + memory_stream_interfere
    interference_threads = interferance_threads + iobench_write_interfere + iobench_read_interfere
    interference_threads = interferance_threads + metadata_interfere
    
    return interference_threads

def create_applications(config):
    
    applications = []
    return applications

def main():

    # TODO, read from command line or config file
    iodir = '/tmp/'
    iotestfile = iodir + 'iobench.file'
    output_file = 'output'

    cores = [0]
   
    # TODO, setup iotest file

    config = { 'cores': cores, 'iotestfile': iotestfile, 'iodir': iodir }
    interference_threads = get_interference_threads(config)
    bmarks = get_benchmarks(config)
    applications = get_applications(config)

    output = {'interference': [], 'application': [], 'y': []}
    
    for thread in interference_threads:
        thread.start()
        try:
            for application in applications:
                
                output['interference'] = str(thread).lower()

                # We permute the bmarks, running 1/2 before and 1/2 after            
                (first, last) = random_partition(bmarks)                           
                application.start_background() # TODO, finish this interface
                
                output = run_benchmarks(first, output)
                output = run_application(application, output)
                output = run_benchmarks(last, output)
        except e:
            pass
            # TODO, do something with the exception here
        
        # Check to ensure that the interference thread was successful
        thread.join()

    # Print our output as needed
    with open(output_file, 'w') as f:
        print_output(f, output)

if __name__=="__main__":

    main()

    
