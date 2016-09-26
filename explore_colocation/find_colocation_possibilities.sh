#!/bin/bash

qos_app=$1
qos_policy=$2
echo $qos_app
echo $qos_policy
./find_colocation_possibilities.py $qos_app $qos_policy > new_experiment_list_${qos_app}_${qos_policy}
