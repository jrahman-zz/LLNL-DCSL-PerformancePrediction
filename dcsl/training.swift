

string interference[] = ["StreamV2Scale", "StreamV2Add", "MemoryV2Stream1K", "MemoryV2Stream256M", "MemoryV2Random1M", "IOBenchV2Read1M", "IOBenchV2Read128M", "IOBenchV2Write4M", "Metadata"];

int reps = 1;

app (file output, file log) run (int rep, string interSpec, string apps) {
    main interSpec @filename(output) stderr=@filename(log);
}

(string threadSpec) createInterfereSpec(string threadName, int colocLevel, int niceLevel) {
    threadSpec = threadName + ":1:" + colocLevel + ":" + niceLevel;
}

type file;
file[string] output;
file[string] logs;

int count = 0;
int colocLevels[] = [0:2];

foreach rep in [1:reps] {
    foreach thread in interference {
        foreach colocLevel in colocLevels {
            int niceLevels[];
            if (colocLevel == 0) {
                niceLevels = [-10, 0, 10];
            } else {
                niceLevels = [0];
            }
            foreach niceLevel in niceLevels {
                string threadspec = createInterfereSpec(thread, colocLevel, niceLevel);
                string runspec = rep + ":" + threadspec;
                
                string oname = strcat("output/run_", runspec, ".json");
                file simout <single_file_mapper; file=name>;
                
                string lname = strcat("output/run_", runspec, ".stdout");
                file simlog <single_file_mapper; file=lname>;
                (simout, simlog) = run(threadspec);
                output[runspec] = simout;
                logs[runspec] = simlog;
            }
        }
    }
}

