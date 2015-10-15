#!/bin/bash

#
# Run REPS repetitions of the experiment on the cab cluster
#

REPS=$1

echo "Launching ${REPS} reps..." 1>&2

JOBS=""
for REP in `seq 1 ${REPS}`; do
OUTFILE="batch.${REP}.sh"    
(
# Build job file
cat <<EOF
#!/bin/bash
#MSUB -l nodes=1
#MSUB -l partition=cab
#MSUB -l walltime=12:00:00
#MSUB -q pbatch
#MSUB -V

cd ~/dcsl/single_app_contention
srun -n1 -N1 -c16 ~/mypy/bin/python ./run_experiments ${REP}    
EOF
) > "${OUTFILE}"

    # Generate experiment list
    ./generate_experiment_list.sh 1 2 > "experiment_list.${REP}"

    echo "Launching rep ${REP}..." 1>&2
    JOB=`msub "${OUTFILE}"`
    if [ $? -ne 0 ]; then
        echo "Error: Failed to submit rep ${REP}" 1>&2
        canceljob ${JOBS}
        exit 1    
    fi
    echo "Launched rep ${REP}" 1>&2
    JOBS="${JOBS} ${JOB}"
done

echo "${JOBS}"
