
if [ $# -lt 1 ]; then
  echo "Error: Need to give experiment name"
  exit 1
fi

EXPERIMENT_PREFIX=$1

for SIZE in 524288 1048576 2097152 4194304 8338608 16777216
do
  echo "Running reporter with size ${SIZE}"
  EXPERIMENT_NAME="${EXPERIMENT_PREFIX}.${SIZE}"
  ./scripts/run_program.sh 1000 "${EXPERIMENT_NAME}.reporter" "./bin/reporter_${SIZE}" 2>1 > /dev/null &
  BACKGROUND_PID=$!
  echo "Started background process with PID = ${BACKGROUND_PID}"
  ./scripts/run_bubble.sh "${EXPERIMENT_NAME}" 1000 250 2500 1 2>1 > /dev/null
  echo "Killing background process with PID = ${BACKGROUND_PID}"
  #kill "${BACKGROUND_PID}"
  pkill -TERM -P ${$}
done
