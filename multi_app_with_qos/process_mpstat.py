#!/usr/bin/env python

import sys
import numpy as np
import glob

def getFileList(dirName)
	pattern = dirName + "/*.mpstat"
	filelist = glob.glob(pattern)
	return filelist
def get_colocation_and_bench(expFileName):
	bname = os.path.basename(expFileName)
	fields = bname.split('.')
	coloc = int(fields[1])
	bmark_apps = fields[2].split('_')
	bmark = ""
	if(len(bmark_apps) == 3):
		bmark = bmark_apps[0]
	else:
		bmark = bmark_apps[0] + bmark_apps[1]
	return (bmark, coloc)

def process_mpstat(f,metric):
    # metric  = usr | sys | iowait | (1 - idle)	
    #print f
    allLines = []
    #We should skip first 3 lines
    f.readline()
    f.readline()
    f.readline()
    for l in f.readlines():
	    l = l.strip()
	    allLines.append(l)
    numLines = len(allLines)
    utilization_dict = {}
    utilization_dict['usr'] = {}
    utilization_dict['sys'] = {}
    utilization_dict['iowait'] = {}
    utilization_dict['total'] = {}
    for line in allLines:	
        fields = line.split()
	timestamp = fields[0]
	cpu = int(fields[1])
	usr = float(fields[2])
	sys = float(fields[4])
	iowait = float(fields[5])
	total = 100.0 - float(fields[10])  # this is 1 - idle field
	if(cpu not in utilization_dict['usr'].keys()):
		utilization_dict['usr'][cpu] = []
		utilization_dict['sys'][cpu] = []
		utilization_dict['iowait'][cpu] = []
		utilization_dict['total'][cpu] = []
	else:
		utilization_dict['usr'][cpu].append(usr)
		utilization_dict['sys'][cpu].append(usr)
		utilization_dict['iowait'][cpu].append(usr)
		utilization_dict['total'][cpu].append(usr)
    #end for
    cpu_dict = {}
    for cpu in utilization_dict[metric].keys():
	    mean_total = np.mean(utilization_dict[metric][cpu])
	    median_total = np.mean(utilization_dict[metric][cpu])
	    #p95_total = np.mean(utilization_dict[metric][cpu])
	    #p99_total = np.mean(utilization_dict[metric][cpu])
	    print cpu, " : " , mean_total, median_total
	    cpu_dict[cpu] = (mean_total, median_total)
    #end for
    return cpu_dict

if __name__ == '__main__':

    #print "process_perf.py called"

    if sys.argv[1] == '--help':
        print('process_mpstat.py experiement mpstat_file metric( = usr | sys | iowait | (1 - idle))')	
        sys.exit(0)
    if len(sys.argv) < 3:
        print('Error: Incorrect argument count')
        sys.exit(1)


    experiment = sys.argv[1]
    perf_filename = sys.argv[2]
    metric = sys.argv[3]

    fileList = getFileList("data_mpistat")
    performance_dict = {}
    for fileName in fileList:
	 (bmark, coloc) = get_colocation_and_bench(fileName)
         with open(fileName, 'r') as f:
        	cpu_dict =  process_mpstat(f,metric)
		(mean_total_utilization, median_total) = cpu_dict[2]
		if(bmark not in performance_dict.keys()):
			performance_dict[bmark] = {}
		if(coloc not in performance_dict[bmark].keys()):
			performance_dict[bmark][coloc] = []

		performance_dict[bmark][coloc].append(mean_total_utilization)
    #end for
    for bmark in performance_dict.keys():
	    for coloc in performance_dict[bmark].keys():
		    mean_of_all_app_utilization = np.mean(performance_dict[bmark][coloc])
		    print "Benchmark: ", bmark, " num of coloc: " , str(coloc), " mean utilization/performance: ", mean_of_all_app_utilization  
    '''
    with open(experiment + ".ipc", 'w') as ipc_f, open(experiment + ".ips", 'w') as ips_f:
        times = sorted(ipc.keys())
        for time in times:
            ipc_f.write('%f %f\n' % (time, ipc[time]))
    '''    
