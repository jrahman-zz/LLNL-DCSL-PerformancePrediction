

string interference[] = ["StreamV2Scale", "StreamV2Add", "MemoryV2Stream1K", "MemoryV2Stream256M", "MemoryV2Random1M", "IOBenchV2Read1M", "IOBenchV2Read128M", "IOBenchV2Write4M", "Metadata"];

string apps = "SpecHRef,SpecGromacs";
string appPath = @arg("appPath");
string dataPath = @arg("dataPath");

int reps = 10;

app (file output, file log) run (int rep, string interSpec, string apps, string dataPath, string appPath) {
    run 3 interSpec apps "training" @filename(output) dataPath appPath stderr=@filename(log);
}

(string threadSpec) createInterfereSpec(string threadName, int colocLevel, int niceLevel) {
    threadSpec = threadName + ":1:" + colocLevel + ":" + niceLevel;
}

type file;
file[string] output;
file[string] logs;

int count = 0;
int colocLevels[] = [0:1];

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
                file simout <single_file_mapper; file=strcat("output/run_", runspec, ".json")>;
                file simlog <single_file_mapper; file=strcat("output/run_", runspec, ".stdout")>;
                (simout, simlog) = run(rep, threadspec, apps, dataPath, appPath);
                output[runspec] = simout;
                logs[runspec] = simlog;
            }
        }
    }
}

