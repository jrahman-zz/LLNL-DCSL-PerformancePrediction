#!/bin/bash
#MSUB -l nodes=1
#MSUB -l partition=cab
#MSUB -l walltime=3:00:00
#MSUB -q pbatch
#MSUB -V

cd "/g/g90/mitra3/scheduling_work/LLNL-DCSL-PerformancePrediction/multi_app_with_qos"
srun -o /p/lscratche/mitra3/job_output/build_sensitivity_curve-%j-%2t.out -n1 -N1 -c16 ~/mypy/bin/python ./run_sensitivity_curve.py redis workloadb 15

