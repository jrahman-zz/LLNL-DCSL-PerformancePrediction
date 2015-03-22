
string apps[] =	[	"SpecBzip",
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

string interference[] = [
					"StreamV2Scale",
					"StreamV2Add",
					"MemoryV2Stream1K",
					"MemoryV2Stream4M",
					"MemoryV2Stream12M",
					"MemoryV2Stream24M",
					"MemoryV2Stream128M",
					"MemoryV2Random1M",
					"MemoryV2Random8M",
					"MemoryV2Random16M",
					"MemoryV2Random32M",
					"IOBenchV2Read1M",
					"IOBenchV2Read128M",
					"IOBenchV2Write4M",
					"Metadata"];

int reps = 10;

app (file output, file log) run (string application, string interSpec) {
    run application interSpec @filename(output) stderr=@filename(log);
}

(string threadSpec) createInterfereSpec(string threadName, int colocLevel, int niceLevel) {
    threadSpec = @strcat(threadName, ":1:", colocLevel, ":", niceLevel);
}

type file;

int count = 0;
int colocLevels[] = [0:2];

foreach application in apps {
	foreach rep in [1:reps] {
		foreach thread in interference {
			foreach colocLevel in colocLevels {
				int niceLevels[];
				if (colocLevel == 0) {
					niceLevels = [0, 5, 10];
				} else {
					niceLevels = [0];
				}
				foreach niceLevel in niceLevels {
					string threadspec = createInterfereSpec(thread, colocLevel, niceLevel);
					string runspec = @strcat(rep, "_", threadspec);
					string basename = @strcat("output/run_", application, "_");	
					string oname = @strcat(basename, runspec, ".json");
					file simout <single_file_mapper; file=oname>;
					string lname = @strcat(basename, runspec, ".stdout");
					file simlog <single_file_mapper; file=lname>;
					(simout, simlog) = run(application, threadspec);
				}
			}
		}
	}
}

