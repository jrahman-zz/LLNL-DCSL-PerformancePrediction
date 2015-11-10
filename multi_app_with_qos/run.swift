type file;

app (file output) run_experiment(string experiment[]) {
    run_experiment experiment;
}

(file output) run(string exp) {
    string tmp[] = strsplit(exp, " ");
    string experiment[];
    foreach v,i in tmp {
        if (i != length(tmp) - 2) {
            experiment[i] = v;
        } else {
            experiment[i] = filename(output);
        }
    }
    trace(experiment);
    trace("\n");
    output = run_experiment(experiment);
}

string runFile = @arg("run.file");
tracef("Opening run file: %s\n", runFile);
string experiments[] = readData(runFile);

foreach experiment in experiments {
    string split[] = strsplit(experiment, " ");
    file simout <single_file_mapper; file=split[length(split)-2]>;
    simout = run(experiment); 
}
