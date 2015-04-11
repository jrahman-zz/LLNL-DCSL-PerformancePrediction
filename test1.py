#!/bin/python

import sys

apps = ["SpecBzip",
		"SpecGcc",
		"SpecGobmk",
		"SpecHmmer",
		"SpecSjeng",
		"SpecLibquantum",
		"SpecHRef",
		"SpecOmnetpp",
		"SpecAstar",
		"SpecXalancbmk",
		"SpecBwaves",
		"SpecMilc",
		"SpecZeusmp",
		"SpecGromacs",
		"SpecCactusADM",
		"SpecLeslie",
		"SpecNamd",
		"SpecSoplex",
		"SpecPovray",
		"SpecCalculix",
		"SpecGemsFDTD",
		"SpecTonto",
		"SpecLbm",
		"SpecWrf",
		"SpecSphinx"];

interference = ["StreamV2Copy",
				"StreamV2Triad",
				"MemoryV2Stream256K",
				"MemoryV2Stream1M",
				"MemoryV2Stream8M",
				"MemoryV2Stream16M",
				"MemoryV2Stream32M",
				"MemoryV2Random1K",
				"MemoryV2Random512K",
				"MemoryV2Random4M",
				"MemoryV2Random12M",
				"MemoryV2Random24M",
				"MemoryV2Random128M",
				"IOBenchV2Read4M",
				"IOBenchV2Write1M",
				"IOBenchV2Write128M"];

reps = range(1, 11)

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
