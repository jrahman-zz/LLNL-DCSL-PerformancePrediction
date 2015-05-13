#!/bin/bash
hostname
use papi
taskset -c 0 ./stream
taskset -c 0 ./whetstone
taskset -c 0 ./dhryestone
taskset -c 0 ./linpack
taskset -c 0 ./lloops
