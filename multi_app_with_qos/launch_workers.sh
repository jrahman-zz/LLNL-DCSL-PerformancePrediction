#1/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: launch.sh nodes hostname port"
    exit 1
fi

NODES=$1
HOSTNAME=$2
PORT=$3
OUTFILE="batch.sh"

OUTPUT_DIR="/p/lscratche/${USER}/job_output"
mkdir -p "${OUTPUT_DIR}"
OUTPUT_PATH="${OUTPUT_DIR}/multi_app_with_qos-%j-%2t.out"

(
cat << EOF
#/bin/bash
#MSUB -l nodes=${NODES}
#MSUB -l partition=cab
#MSUB -l walltime=12:00:00
#MSUB -q pbatch
#MSUB -V

cd "${PWD}"
srun -o ${OUTPUT_PATH} -n${NODES} -N${NODES} -c16 ~/mypy/bin/python ./run_experiment.py ${HOSTNAME} ${PORT}

EOF
) > "${OUTFILE}"

echo `msub "${OUTFILE}"`
