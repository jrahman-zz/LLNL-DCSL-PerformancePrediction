#!/bin/bash

#how to run? create_experiments.py REPS CORES MAXAPPS
./create_experiment.py 1 1 2 > experiment_list

#give a unique port number
./run_master 13456 

#give the hostname and port number of the master
./run_experiment.py cab690 13456
