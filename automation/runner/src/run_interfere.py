from stream import StreamCopyInterfere, StreamAddInterfere, StreamScaleInterfere, StreamTriadInterfere
from memory import MemoryStream1KInterfere, MemoryStream1MInterfere, MemoryStream1GInterfere
from memory import MemoryRandom1KInterfere, MemoryRandom1MInterfere, MemoryRandom1GInterfere

import gevent

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def stream_suite():
    cores = [0, 2]
    threads = [StreamCopyInterfere(cores), StreamAddInterfere(cores), StreamScaleInterfere(cores), StreamTriadInterfere(cores)]

    # Kick off greenlets
    for thread in threads:
        thread.start()

    gevent.sleep(30)
    logging.info('Joining again')
    
    # Join back in
    for thread in threads:
        thread.join()

def memory_stream_suite():
    cores = [1, 3]
    threads = [MemoryStream1KInterfere(cores), MemoryStream1MInterfere(cores), MemoryStream1GInterfere(cores)]

    for thread in threads:
        thread.start()

    gevent.sleep(180)

    for thread in threads:
        bmark.join()

def memory_random_suite():
    cores = [0, 2]
    threads = [MemoryRandom1KInterfere(cores), MemoryRandom1MIntefere(cores), MemoryRandom1GInterfere(cores)]

    for thread in threads:
        thread.start()

    gevent.sleep(40)
    
    for thread in threads:
        thread.join()

def main():
    stream_suite()


if __name__ == '__main__':
    main()
