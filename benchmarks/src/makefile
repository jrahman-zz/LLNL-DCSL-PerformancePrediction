CC = gcc
CPP = g++

PAPI_PATH=/usr/lib/x86_64-linux-gnu/

COMMON = -L$(PAPI_PATH)/libpapi.so.5.3 -l:libpapi.so.5.3 -Wl,-rpath,$(PAPI_PATH)

CFLAGS = -Wall -g
CPPFLAGS = -Wall -std=c++11

PAPI_OBJS = papi_util.o papi_counters.o perf_counters.o

STREAM_FLAGS = -O2 $(COMMON) -DCOUNTERS
STREAMV2_FLAGS = -O0 $(COMMON)
METADATA_FLAGS = -lrt $(COMMON)
MEMORY_FLAGS = -lrt $(COMMON)
MEMORYV2_FLAGS = -lrt -DV2 -DREGULAR_STRIDE=64 -DRANDOM_STRIDE=512 -DBANDWIDTH_SCALE=100000 $(COMMON)

DHRYSTONE_FLAGS = -m64 -lrt -lc -lm -DCOUNTERS $(COMMON)
WHETSTONE_FLAGS = -m64 -lrt -lc -lm -DCOUNTERS $(COMMON)
LIVERMORE_FLAGS = -m64 -lrt -lc -lm
LINPACK_FLAGS = -m64 -lrt -lc -lm

PAPI_FLAGS = -std=c99 $(COMMON)

all: build

build: benchmarks interference test

.PHONY: benchmarks
benchmarks: stream streamV2 metadata memory memoryV2 dhrystone whetstone lloops linpack

.PHONY: interference
interference: stream_interfere streamV2_interfere metadata_interfere memory_interfere memoryV2_interfere

# Stream
stream: stream.c $(PAPI_OBJS)
	$(CC) $(CFLAGS) stream.c $(PAPI_OBJS) $(STREAM_FLAGS) -o stream

stream_interfere: stream.c $(PAPI_OBJS)
	$(CC) $(CFLAGS) stream.c $(STREAM_FLAGS) -DINTERFERE -o stream_interfere

# Stream V2
streamV2: stream.c $(PAPI_OBJS)
	$(CC) $(CFLAGS) stream.c $(PAPI_OBJS) $(STREAMV2_FLAGS) -DNTIMES=100000 -o streamV2

streamV2_interfere: stream.c $(PAPI_OBJS)
	$(CC) $(CFLAGS) stream.c $(STREAMV2_FLAGS) -DINTERFERE -DNTIMES=100000 -o streamV2_interfere

# Metadata
metadata: metadata.cpp $(PAPI_OBJS)
	$(CPP) $(CPPFLAGS) metadata.cpp $(METADATA_FLAGS) -o metadata

metadata_interfere: metadata.cpp
	$(CPP) $(CPPFLAGS) metadata.cpp $(METADATA_FLAGS) -DINTERFERE -o metadata_interfere

# Memory
memory: memory.o identity.o $(PAPI_OBJS)
	$(CPP) $(CPPFLAGS) $(PAPI_OBJS) memory.o identity.o $(MEMORY_FLAGS) -o memory

memory_interfere: memory_interfere.o identity.o
	$(CPP) $(CPPFLAGS) memory_interfere.o identity.o $(MEMORY_FLAGS) -o memory_interfere

memory.o: memory.cpp 
	$(CPP) $(CPPFLAGS) memory.cpp $(MEMORY_FLAGS) -c -o memory.o

memory_interfere.o: memory.cpp
	$(CPP) $(CPPFLAGS) memory.cpp $(MEMORY_FLAGS) -DINTERFERE -c -o memory_interfere.o

identity.o: identity.cpp
	$(CPP) $(CPPFLAGS) -c -o identity.o identity.cpp

# Memory V2
memoryV2: memoryV2.o identity.o $(PAPI_OBJS)
	$(CPP) $(CPPFLAGS) memoryV2.o identity.o $(PAPI_OBJS) $(MEMORYV2_FLAGS) -o memoryV2

memoryV2_interfere: memoryV2_interfere.o identity.o
	$(CPP) $(CPPFLAGS) memoryV2_interfere.o identity.o $(MEMORYV2_FLAGS) -o memoryV2_interfere

memoryV2.o: memory.cpp
	$(CPP) $(CPPFLAGS) memory.cpp $(MEMORYV2_FLAGS) -c -o memoryV2.o

memoryV2_interfere.o: memory.cpp
	$(CPP) $(CPPFLAGS) memory.cpp $(MEMORYV2_FLAGS) -DINTERFERE -c -o memoryV2_interfere.o

# Dhrystone
dhrystone: dhry_1.c dhry_2.c cpuidc64.o $(PAPI_OBJS)
	$(CC) dhry_1.c dhry_2.c cpuidc64.o $(PAPI_OBJS) $(DHRYSTONE_FLAGS) -o dhrystone

# Whetstone
whetstone: whets.c cpuidc64.o $(PAPI_OBJS)
	$(CC) whets.c cpuidc64.o $(PAPI_OBJS) $(WHETSTONE_FLAGS) -o whetstone

# Livermore loops
lloops: lloops.c cpuidc64.o
	$(CC) lloops.c cpuidc64.o $(LIVERMORE_FLAGS) -o lloops

# Linpack
linpack: linpack.c cpuidc64.o
	$(CC) linpack.c cpuidc64.o $(LINPACK_FLAGS) -g -o linpack

cpuidc64.o:
	$(CC) cpuidc64.c -c

# Papi
papi_util.o: papi_util.c papi_util.h
	$(CC) $(CFLAGS) papi_util.c $(PAPI_FLAGS) -c -o papi_util.o

papi_counters.o: papi_counters.c papi_util.h
	$(CC) $(CFLAGS) papi_counters.c $(PAPI_FLAGS) -c -o papi_counters.o

# Perf counters
perf_counters.o: perf_counters.c perf_counters.h papi_util.h papi_util.o
	$(CC) $(CFLAGS) perf_counters.c $(PAPI_FLAGS) -c -o perf_counters.o

test: test.c $(PAPI_OBJS)
	$(CC) $(CFLAGS) $(PAPI_OBJS) test.c $(COMMON) -o test

clean:
	rm *.o
	rm -f stream
	rm -f stream_interfere
	rm -f streamV2
	rm -f streamV2_interfere
	rm -f metadata
	rm -f memory
	rm -f memory_interfere
	rm -f memoryV2
	rm -f memoryV2_interfere
	rm -f test



