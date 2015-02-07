#!/bin/bash


function usage {
    echo "Usage: setup.sh YCSB_DIR MONGODB_DIR DATA_DIR PID_FILE"
}

if [ $# -ne 5 ]; then
    usage
    exit 1
fi

# Path to base of YCSB dir
YCSB_DIR=${1}
if [ ! -d "${YCSB_DIR}" ]; then
    echo "Error: YCSB directory doesn't exist"
    usage
    exit 1
fi

if [ ! -x "${YCSB_DIR}/bin/ycsb" ]; then
    echo "Error: YCSB directory is incorrect"
    usage
    exit 1
fi

# Path
MONGODB_DIR=${2}
if [ ! -d "${MONGODB_DIR}" ]; then
    echo "Error: MongoDB directory doesn't exist"
    usage
    exit 1
fi

if [ ! -f "${MONGODB_DIR}/bin/mongod" -o ! -x "${CASSANDRA_DIR}/bin/cassandra-cli" ]; then
    echo "Error: MongoDB directory is incorrect"
    usage
    exit 1
fi

# Path to directory to store data directory
DATA_DIR=${3}
if [ ! -d "${DATA_DIR}" ]; then
    echo "Error: Data parent directory doesn't exist"
    usage
    exit 1
fi

# Name of PID file
PID_FILE=${4}


# Tweak the config file...
echo "Customizing configuration..."
cp "config.yaml" "config.yaml.custom"
if [ $? -ne 0 ]; then
    echo "Error: Failed to copy config"
    exit 1
fi
DBLOCATION="${DATA_DIR}/mongodb_data/"
sed -e -i "s,<SYSTEMLOG>,${DBLOCATION},g" "config.yaml.custom"
if [ $? -ne 0 ]; then
    echo "Error: Failed to customize config file"
    exit 1
fi
sed -e -i "s,<DBPATH>,${DBLOCATION},g" "config.yaml.custom"
if [ $? -ne 0 ]; then
    echo "Error: Failed to customize config file"
    exit 1
fi
echo "Customized configuration file"


echo "Starting server..."
${MONGODB_DIR}/bin/mongod --pidfilepath "${PIDFILE}" --fork --config "config.yaml.custom"
if [ $? -ne 0 ]; then
    echo "Error: Failed to start mongodb"
    exit 1
fi

exit 0
