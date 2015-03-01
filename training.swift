
type outfile

string interference[] = ["", "", ""]
int replications = 10

app (outfile output) run (int replication, string interference_spec, string data_path, string app_path) {
    run_sh 3 interference_spec @filename(outout) data_path app_path
}

(string thread_spec) create_interfere_spec(string thread_name, int coloc_level, int nice_level) {
    thread_spec = thread_name + ":1:" + coloc_level + ":" + nice_level
}

int coloc_levels[] = [0:2]
int nice_levels[] = [-10, 0, 10]

outfile[string] output;

foreach replication in [1:replications] {
    foreach thread in interference {
        foreach coloc_level in coloc_levels {
            int nice_levels
            if (coloc_level == 0) {
                nice_levels = [-10, 0, 10]
            } else {
                nice_levels = [0]
            }
            foreach nice_level in nice_levels {
                threadspec = create_interfere_spec(thread, coloc_level, nice_level)
                runspec = replication + ":" + threadspec
                output[runspec] = run(replication, threadspec, data_path, app_path)
            }
        }
    }
}

