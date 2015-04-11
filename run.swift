type RunConfig {
	string application;
	string interference;
	string log_file;
	string output_file;
}

type file;

app (file output, file log) run (string application, string interference) {
	run application interference @filename(output) stderr=@filename(log);
}

string runFile = @arg("run.file");
tracef("Opening run file: %s", runFile);
RunConfig runs[] = readData(runFile);

foreach run in runs {
	file simout <single_file_mapper; file=run.output_file>;
	file simlog <single_file_mapper; file=run.log_file>;
	string application = run.application;
	string interference = run.interference;
	(simout, simlog) = run(application, interference); 
}
