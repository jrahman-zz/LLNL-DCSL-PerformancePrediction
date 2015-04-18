#!/bin/python

import sys
import itertools

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
        "SpecSphinx:1"]

interference = apps

reps = range(1, 6)

def create_interfere_spec(thread_name, coloc_level, nice_level):
    return "%s:1:%d:%d" % (thread_name, coloc_level, nice_level)

count = 0
coloc_levels = range(0, 3)

def generate_list():
	global apps

	# Track iterations per interference counts
	counts = {}
	fractions = {}

	output = {'interference': [], 'application': [], 'output_file': [], 'log_file': []}
	configs = []
	coloc_levels = [0, 1, 2]
	for coloc_level in coloc_levels:
		if (coloc_level == 0):
			nice_levels = [0, 5, 10]
		else:
			nice_levels = [0]
		for nice_level in nice_levels:
			configs.append({'coloc_level': coloc_level, 'nice_level': nice_level})

	total = 0

	# Calculate the number of configurations and splittings first
	max_interfere = 3
	for count in range(1, max_interfere+1):
		counts[count] = 0
		unique_configs = itertools.permutations(configs, count)
		
		filtered = map(lambda entry: entry[1], filter(lambda agg: agg[0] <= 1, map(lambda config: reduce(lambda tup, x: tuple(map(lambda a, b: a + b, (x['coloc_level'] == 0, [x]), tup)), config, (0, [])), unique_configs)))
		for config in filtered:
			app_combinations = itertools.permutations(interference, count)
			for perm in app_combinations:
				counts[count] = counts[count] + 1
				total = total + 1

	target = 250
	target_per_count = target / len(counts.keys())

	for count in counts.keys():
		fractions[count] = max(counts[count] / target_per_count, 1)

	print(target_per_count)
	print(counts)
	print(fractions)

	total = 0

	# Sample over number of interfering applications
	for count in range(1, max_interfere+1):
	
		# Reset counts
		counts[count] = 0

		unique_configs = itertools.permutations(configs, count)
	
		# Build dummy padding
		padding = []
		for i in range(0, max_interfere - count + 1):
			padding.append("Dummy:1:0:0")
		
		# Filter out any configs with more than one entry with colocation level 0
		# No, this is not a sick joke (ok, so it sort of is, but it actually works)
		filtered = map(lambda entry: entry[1], filter(lambda agg: agg[0] <= 1, map(lambda config: reduce(lambda tup, x: tuple(map(lambda a, b: a + b, (x['coloc_level'] == 0, [x]), tup)), config, (0, [])), unique_configs)))

		# Sample over permations of different configurations
		for config in filtered:
			app_permutations = itertools.permutations(interference, count)

			# Sample over different assignments of interference threads to configurations
			for perm in app_permutations:
			
				# Skip over counts
				counts[count] = counts[count] + 1
				if counts[count] % fractions[count] != 0:
					continue
	
				total = total + 1
				if total % 100:
					print('Done with %d' % total)

				tspecs = map(lambda app, conf: "%s:1:%d:%d" % (app, conf['coloc_level'], conf['nice_level']), perm, config)
				
				# Pad with dummy interference
				tspec = ','.join(tspecs + padding)
				for application in apps:
					for rep in reps:
						runspec = "%d_%s" % (rep, tspec)
						basename = "output/run_" + application + "_"	
						oname = basename + runspec + ".json"
						lname = basename + runspec + ".stdout"
						output['interference'].append(tspec)
						output['output_file'].append(oname)
						output['log_file'].append(lname)
						output['application'].append(application)

	return output
					
def write_to_file(filename, data):
	with open(filename, 'w') as f:
		keys = data.keys()
		keys.sort()
		print(len(data[keys[0]]))
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
