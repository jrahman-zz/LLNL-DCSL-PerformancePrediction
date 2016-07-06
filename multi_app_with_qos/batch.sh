#/bin/bash
#MSUB -l nodes=16
#MSUB -l partition=cab
#MSUB -l walltime=1:00:00
#MSUB -q pbatch
#MSUB -V

cd "/g/g90/mitra3/scheduling_work/LLNL-DCSL-PerformancePrediction/multi_app_with_qos"
srun -o /p/lscratche/mitra3/job_output/multi_app_with_qos-%j-%2t.out -n16 -N16 -c16 ~/mypy/bin/python ./run_experiment.py cab690 13456

