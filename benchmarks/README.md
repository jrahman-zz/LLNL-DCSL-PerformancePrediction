
# Benchmark Descriptions

Below are descriptions of the various microbenchmarks that are currently available.

## Stream
[Stream Source Code](src/stream.c)
[Stream Automation Source Code](../automation/benchmarks/stream.py)
Stream is a memory intensive benchmark for stressing memory bandwidth and cache
[Stream Homepage](http://www.cs.virginia.edu/stream/)
It exercises a sequential memory access pattern with an out of cache working set.

##
[Memory Benchmark Source Code](src/memory.cpp)
[Memory Automation Source Code](../automation/benchmarks/memory.py)
Memory is a general memory benchmark from Bowen's original tarball (Believe it came from Marc Casas).
It contains multiple operation modes stressing sequential and random access patterns.
Since stream already measures sequential access, we only use the random access mode.

## Dhrystone
[Dhrystone Benchmark Source Code](src/dhry_1.c)
[Dhrystone Automation Source Code](../automation/runner/benchmarks/dhrystone.py)
Dhrystone is a synthetic microbenchmark that stresses integer and branch operations.
Lots of branches, pointer dereference operations
It is intended to simulate a typical "systems programming" workload.

## Whetstone
[Whetstone Benchmark Source Code](src/whets.c)
[Whetstone Automation Source Code](../automation/runner/benchmarks/whetstone.py)
Whetstone is a synthetic microbenchmark written in C that stresses a machines floating point performance.

## Livermore Loops
[Livermore Loops Source Code](src/lloops.c)
[Livermore Loops Automation Source Code](../automation/runner/benchmarks/livermore.py)
Livermore loops are a set of core common scientific computation kernels.
Mainly various matrix operations, numerical intergration, ODE solvers, etc.
Smaller WSS ~1KB-1MB so mainly arithmetic.

## Linpack
[Linpack Benchmark Source Code](src/linpack.c)
[Linpack Automation Source Code](../automation/runner/benchmarks/linpack.py)
Miniature version of the popular benchmark application.
Performs various matrix and linear algebra routines on small (~100x100 matrices)
Stresses the L1 and L2 caches, and the double precision floating point units

## IOBench
[IOBench Source Code](iobench/src)
[IOBenchmark Automation Source Code](../automation/runner/benchmarks/iobench.py)
IOBench is a simple disk IO performance benchmark that stresses either read or write workloads.
Several different workloads are implemented, including read and write workloads of sizes 1MB, 4MB and 128MB.
[IOBench Homepage](https://github.com/scalyr/iobench)

## Metadata
[Metadata Benchmark Source Code](src/metadata.cpp)
[Metadata Automation Source Code](../automation/runner/benchmarks/metadata.py)
The metadata benchmark creates and deletes a large number of files (currently 1000), and performs the associated disk flushes to persist the changes to the metadata.
