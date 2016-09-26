#!/bin/bash
#MSUB -l nodes=1
#MSUB -l partition=cab
#MSUB -l walltime=15:30:00
#MSUB -q pbatch
#MSUB -V

OUTPUT_PATH="./job_out-%j-%2t.out"
cd "${PWD}"
srun -o ${OUTPUT_PATH} -n1 -N1 -c16 ./process_experiments.py 14 > processed_experiments_mongodb_july19
