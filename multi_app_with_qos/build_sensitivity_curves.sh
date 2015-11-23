#!/bin/bash

NODES=1

for REP in `seq 1 5`; do
    while read LINE; do
        IFS=' ' read -r -a QOS <<< "${LINE}"
        OUTPUT_FILE="${QOS[0]}.${REP}.sh"
        {
            cat << EOL
#!/bin/bash
#MSUB -l nodes=1
#MSUB -l partition=cab
#MSUB -l walltime=5:00:00
#MSUB -q pbatch
#MSUB -V

cd "${PWD}"
srun -n${NODES} -N${NODES} -c16 ~/mypy/bin/python ./run_sensitivity_curve.py ${LINE} ${REP}
EOL
} > "${OUTPUT_FILE}"
    done < manifest/qos
done
