#/bin/bash
#MSUB -l nodes=2
#MSUB -l partition=cab
#MSUB -l walltime=12:00:00
#MSUB -q pbatch
#MSUB -V

cd "/g/g90/mitra3/scheduling_work/LLNL-DCSL-PerformancePrediction/multi_app_contention"
srun -o /p/lscratche/mitra3/job_output/multi_app_contention-%j-%2t.out -n2 -N2 -c16 ~/mypy/bin/python ./run_experiment.py cab690 13456

