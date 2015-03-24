
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
					"StreamV2Copy",
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

int reps = 3;

app (file output, file log) run_test1 (string application, string interSpec) {
    run_test1 application interSpec @filename(output) stderr=@filename(log);
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
					(simout, simlog) = run_test1(application, threadspec);
				}
			}
		}
	}
}

