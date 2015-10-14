#!/bin/env python

import sys

# Returns IPC and IPS as indexed by time
def process_perf(f):
    start_time = float(f.readline().strip())
    cycles = dict()
    instructions = dict()
    ipc = dict()
    ips = dict()
    for line in f:
        values = line.strip().split()
        if values[2] == 'instructions':
            time = float(values[0])
            instructions[time] = int(values[1])
        elif values[2] == 'cycles':
            time = float(values[0])
            cycles[time] = int(values[1])
    if set(cycles.keys()) != set(instructions.keys()):
        raise Exception('Some timesteps missing either cycles or instructions')
    times = sorted(cycles.keys())
    prev_time = 0
    for time in times:
        absolute_time = time + start_time
        ips[absolute_time] = float(instructions[time]) / float(time - prev_time)
        ipc[absolute_time] = float(instructions[time]) / float(cycles[time])
        prev_time = time
    return (ips, ipc)

if __name__ == '__main__':
    if sys.argv[1] == '--help':
        print('process.py experiement perf_file')
        sys.exit(0)
    if len(sys.argv) < 3:
        print('Error: Incorrect argument count')
        sys.exit(1)

    experiment = sys.argv[1]
    perf_filename = sys.argv[2]
    with open(perf_filename, 'r') as f:
        (ips, ipc) = process_perf(f)
    
    with open(experiment + ".ipc", 'w') as ipc_f, open(experiment + ".ips", 'w') as ips_f:
        times = sorted(ipc.keys())
        for time in times:
            ipc_f.write('%f %f\n' % (time, ipc[time]))
            ips_f.write('%f %f\n' % (time, ips[time]))
        
