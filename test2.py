#!/bin/python

import sys
import itertools

apps = ["SpecBzip",
		"SpecGcc",
		"SpecGobmk",
		"SpecHMMER",
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

interference = apps

reps = range(1, 11)

def create_interfere_spec(thread_name, coloc_level, nice_level):
    return "%s:1:%d:%d" % (thread_name, coloc_level, nice_level)

count = 0
coloc_levels = range(0, 3)

def generate_list():
	output = {'interference': [], 'application': [], 'output_file': [], 'log_file': []}
	configs = []
	for coloc_level in coloc_levels:
		if (coloc_level == 0):
			nice_levels = [0, 5, 10]
		else:
			nice_levels = [0]
		for nice_level in nice_levels:
			configs.append({'coloc_level': coloc_level, 'nice_level': nice_level})

	total = 0

	# Sample over number of interfering applications
	max_interfere = 3
	for count in range(1, max_interfere+1):
		unique_configs = itertools.combinations_with_replacement(configs, count)
	
		# Build dummy padding
		padding = []
		for i in range(0, max_interfere - count):
			padding.append("Dummy:1:0:0")
		
		# Filter out any configs with more than one entry with colocation level 0
		# No, this is not a sick joke (ok, so it sort of is, but it actually works)
		filtered = map(lambda entry: entry[1], filter(lambda agg: agg[0] <= 1, map(lambda config: reduce(lambda tup, x: tuple(map(lambda a, b: a + b, (x['coloc_level'] == 0, [x]), tup)), config, (0, [])), unique_configs)))

		# Sample over combination of different configurations
		for config in filtered:
			print(config)
			app_permutations = itertools.combinations(interference, count + 1)

			# Sample over different assignments of interference threads to configurations
			for perm in app_permutations:
				total = total + 1

				# Uniformly sample every 500th configuration
				if total % 500 != 0:
					continue

				application = perm[0]
				perm = perm[1:len(perm)]
				tspecs = map(lambda app, conf: "%s:1:%d:%d" % (app, conf['coloc_level'], conf['nice_level']), perm, config)
				
				# Pad with dummy interference
				tspec = ','.join(tspecs + padding)
				for rep in reps:
					runspec = "%d_%s" % (rep, tspec)
					basename = "output/run_" + application + "_"	
					oname = basename + runspec + ".json"
					lname = basename + runspec + ".stdout"
					output['interference'].append(tspec)
					output['output_file'].append(oname)
					output['log_file'].append(lname)
					output['application'].append(application)

	print(total)
	print(len(output['application']))
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
