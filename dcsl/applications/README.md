Interface scripts for applications are located within this directory.

Each application must define 5 different interface scripts:
  * load.sh
  * start.sh
  * run.sh
  * stop.sh
  * cleanup.sh
  
Each script is run at a certain time for a certain purpose.

APPLICATION_DIRECTORY refers to the directory where the given application was installed
This value is specified in automation/runner/src/applications.json for each application and is system specific

### load.sh APPLICATION_DIRECTORY DATA_DIRECTORY ....
This script is run only once, when the worker is initialized.
Typical actions this script can take may include:
  * Populating or generating benchmark datasets
  * Creating a set of sub-directories in DATA_DIRECTORY

### start.sh APPLICATION_DIRECTORY DATA_DIRECTORY ....
This script is run everytime the application is about to be run, immediately before it is to be executed.
Typical actions this script can take may include:
  * Starting a background server on which the tests will run
  * Moving a dataset into location for use

### run.sh APPLICATION_DIRECTORY DATA_DIRECTORY ....
This script should actually run the benchmark.
The output from this command is parsed to extract the performance information we later analyse.

### stop.sh APPLICATION_DIRECTORY DATA_DIRECTORY ....
This script is run immediately following run.sh, and performs basic cleanup operations.
Typical actions this script can take may include:
  * Stoping the background server on which the tests ran
  * Cleaning up temporary files

### cleanup.sh APPLICATION_DIRECTORY DATA_DIRECTORY ....

