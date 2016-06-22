#!/bin/bash

NODES=1

OUTPUT_DIR="/p/lscratche/${USER}/job_output"
mkdir -p "${OUTPUT_DIR}"
OUTPUT_PATH="${OUTPUT_DIR}/standalone_qos_app-%j-%2t.out"

for REP in `seq 1 25`; do
    while read LINE; do
        IFS=' ' read -r -a QOS <<< "${LINE}"
        OUTPUT_FILE="${OUTPUT_DIR}/standalone_${QOS[0]}.${REP}.sh"
        {
            cat << EOL
#!/bin/bash
#MSUB -l nodes=1
#MSUB -l partition=cab
#MSUB -l walltime=3:00:00
#MSUB -q pbatch
#MSUB -V

cd "${PWD}"
srun -o ${OUTPUT_PATH} -n${NODES} -N${NODES} -c16 ~/mypy/bin/python ./run_standalone_qos_app.py ${LINE} ${REP}

EOL
} > "${OUTPUT_FILE}"
        msub "${OUTPUT_FILE}"
    done < manifest/qos
done
