#!/bin/bash
uname -a
cat /proc/cpuinfo | tail -n24
cat /proc/meminfo

cd src/bin
for i in $(seq 0 20)
# nice cpu%
#    0   50
#   10   10
#   20    0
do
  if [ $i -le 20 ]
  then
    taskset -c 0 nice -n $i ./hog &
  fi

  exec >../../log.$i

  taskset -c 0 ./tsp A_40.txt x_40.txt x_40.txt Ax.txt Atx.txt
  taskset -c 0 ./td 40 40 A_40.txt x_40.txt x_40.txt Ax.txt Atx.txt
  taskset -c 0 ./alloctest 1 100000 1000 1000
  taskset -c 0 ./example 0 1000 10  # Bandwidth size repeat
  taskset -c 0 ./example 1 1000 10  # Regular access size repeat
  taskset -c 0 ./example 2 1000 1   # Random access size repeat
  taskset -c 0 ./example 3 1000 10  # Compress branch size repeat
  taskset -c 0 ./filetest A_40.txt 100000

  exec >&-

  pkill hog
done
