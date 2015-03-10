
# Benchmark Descriptions

Below are descriptions of the various microbenchmarks that are currently available.

## Stream
* Benchmark: [Stream Source Code](src/stream.c)
* Automation: [Stream Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/stream.py)
* Metric Generated: MB/s

Stream is a memory intensive benchmark for stressing memory bandwidth and cache
[Stream Homepage](http://www.cs.virginia.edu/stream/)
It exercises a sequential memory access pattern with an out of cache working set.

## Memory (Random)
* Benchmark: [Memory Benchmark Source Code](src/memory.cpp)
* Automation: [Memory Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/memory.py)
* Metric Generated: runtime

Memory is a general memory benchmark from Bowen's original tarball (Believe it came from Marc Casas).
It contains multiple operation modes stressing sequential and random access patterns.
Since stream already measures sequential access, we only use the random access mode.

## Dhrystone
* Benchmark: [Dhrystone Benchmark Source Code](src/dhry_1.c)
* Automation: [Dhrystone Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/dhrystone.py)
* Metric Generated: Psuedo-MIPS (MIPS based on reference)

Dhrystone is a synthetic microbenchmark that stresses integer and branch operations.
Lots of branches, pointer dereference operations
It is intended to simulate a typical "systems programming" workload.

## Whetstone
* Benchmark: [Whetstone Benchmark Source Code](src/whets.c)
* Automation: [Whetstone Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/whetstone.py)
* Metric Generated: mwips (mega whetstone operations per second), and various other OPs per second (trig. ops, flops, ifops, eqops, etc)

Whetstone is a synthetic microbenchmark written in C that stresses a machines floating point performance.

## Livermore Loops
* Benchmark: [Livermore Loops Source Code](src/lloops.c)
* Automation: [Livermore Loops Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/livermore.py)
* Metric Generated: Various averges (arithmetic, harmonic, geometric, etc) of flop values for different kernels.

Livermore loops are a set of core common scientific computation kernels.
Mainly various matrix operations, numerical intergration, ODE solvers, etc.
Smaller WSS ~1KB-1MB so mainly arithmetic.

## Linpack
* Benchmark: [Linpack Benchmark Source Code](src/linpack.c)
* Automation: [Linpack Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/linpack.py)
* Metric Generated: mflops

Miniature version of the popular benchmark application.
Performs various matrix and linear algebra routines on small (~100x100 matrices)
Stresses the L1 and L2 caches, and the double precision floating point units

## IOBench
* Benchmark: [IOBench Source Code](iobench/src)
* Automation: [IOBenchmark Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/iobench.py)
* Metric Generated: operation runtime (latency) (mean and 99th percentile)

IOBench is a simple disk IO performance benchmark that stresses either read or write workloads.
Several different workloads are implemented, including read and write workloads of sizes 1MB, 4MB and 128MB.
[IOBench Homepage](https://github.com/scalyr/iobench)

## Metadata
* Benchmark: [Metadata Benchmark Source Code](src/metadata.cpp)
* Automation: [Metadata Automation Source Code](https://github.com/jrahman/LLNL-DCSL-PerformancePrediction/tree/master/automation/runner/benchmarks/metadata.py)
* Metric: runtime (median and 99th percentile)

The metadata benchmark creates and deletes a large number of files (currently 1000), and performs the associated disk flushes to persist the changes to the metadata.
