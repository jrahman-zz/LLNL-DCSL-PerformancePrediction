#!/bin/python

import sys

apps = ["SpecBzip:1",
        "SpecGcc:1",
        "SpecGobmk:1",
        "SpecHmmer:1",
        "SpecSjeng:1",
        "SpecLibquantum:1",
        "SpecHRef:1",
        "SpecOmnetpp:1",
        "SpecAstar:1",
        "SpecXalancbmk:1",
        "SpecBwaves:1",
        "SpecMilc:1",
        "SpecZeusmp:1",
        "SpecGromacs:1",
        "SpecCactusADM:1",
        "SpecLeslie:1",
        "SpecNamd:1",
        "SpecSoplex:1",
        "SpecPovray:1",
        "SpecCalculix:1",
        "SpecGemsFDTD:1",
        "SpecTonto:1",
        "SpecLbm:1",
        "SpecWrf:1",
        "SpecSphinx:1"];

interference = ["StreamV2Scale",
				"StreamV2Add",
				"MemoryV2Stream1K",
				"MemoryV2Stream512K",
				"MemoryV2Stream4M",
				"MemoryV2Stream12M",
				"MemoryV2Stream24M",
				"MemoryV2Random256K",
				"MemoryV2Random1M",
				"MemoryV2Random8M",
				"MemoryV2Random16M",
				"MemoryV2Random32M",
				"IOBenchV2Read1M",
				"IOBenchV2Read128M",
				"IOBenchV2Write4M"];

reps = range(0, 11)

def create_interfere_spec(thread_name, coloc_level, nice_level):
    return "%s:1:%d:%d" % (thread_name, coloc_level, nice_level)


count = 0
colocLevels = range(0, 3)

def generate_list():
	output = {'interference': [], 'application': [], 'output_file': [], 'log_file': []}
	for application in apps:
		for rep in reps:
			for thread in interference:
				for colocLevel in colocLevels:
					if (colocLevel == 0):
						niceLevels = [0, 5, 10]
					else:
						niceLevels = [0]
					for niceLevel in niceLevels:
						threadspec = create_interfere_spec(thread, colocLevel, niceLevel)
						runspec = "%d_%s" % (rep, threadspec)
						basename = "output/run_" + application + "_"	
						oname = basename + runspec + ".json"
						lname = basename + runspec + ".stdout"
						output['interference'].append(threadspec)
						output['output_file'].append(oname)
						output['log_file'].append(lname)
						output['application'].append(application)
	return output
					
def write_to_file(filename, data):
	with open(filename, 'w') as f:
		keys = data.keys()
		keys.sort()
		header = " ".join(keys)
		f.write(header + "\n")
		while len(data[keys[0]]) > 0:
			line = []
			for key in keys:
				line.append(data[key].pop(0))
			line = " ".join(line)
			f.write(line + "\n")

def main(output_file):
	data = generate_list()
	write_to_file(output_file, data)

if __name__ == "__main__":
	output_file = sys.argv[1]
	main(output_file)			  
