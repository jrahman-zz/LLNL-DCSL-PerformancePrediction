#/bin/bash
#MSUB -l nodes=10
#MSUB -l partition=cab
#MSUB -l walltime=15:00:00
#MSUB -q pbatch
#MSUB -V

cd "/g/g19/rahman3/DCSL/multi_app_contention"
srun -n10 -N10 -c16 ~/mypy/bin/python ./run_experiment.py cab668 18129

