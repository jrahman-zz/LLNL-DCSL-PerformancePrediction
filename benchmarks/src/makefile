CC = gcc
CPP = g++

CFLAGS = -Wall
CPPFLAGS = -Wall -std=c++11

STREAM_FLAGS = -O2
STREAMV2_FLAGS = -O0
METADATA_FLAGS = -lrt
MEMORY_FLAGS = -lrt
MEMORYV2_FLAGS = -lrt -DV2 -DREGULAR_STRIDE=1024 -DRANDOM_STRIDE=512 -DBANDWIDTH_SCALE=100000
PAPI_FLAGS = -std=c99

all: build

build: benchmarks interference

.PHONY: benchmarks
benchmarks: stream streamV2 metadata memory memoryV2

.PHONY: interference
interference: stream_interfere streamV2_interfere metadata memory memoryV2

# Stream
stream: stream.c
	$(CC) $(CFLAGS) $(STREAM_FLAGS) stream.c -o stream

stream_interfere: stream.c
	$(CC) $(CFLAGS) $(STREAM_FLAGS) stream.c -o stream_interfere

# Stream V2
streamV2: stream.c
	$(CC) $(CFLAGS) $(STREAMV2_FLAGS) stream.c -DNTIMES=100000 -o streamV2

streamV2_interfere: stream.c
	$(CC) $(CFLAGS) $(STREAMV2_FLAGS) stream.c -DNTIMES=100000 -o streamV2_interfere

# Metadata
metadata: metadata.cpp
	$(CPP) $(CPPFLAGS) metadata.cpp $(METADATA_FLAGS) -o metadata

# Memory
memory: memory.o identity.o
	$(CPP) $(CPPFLAGS) $(MEMORY_FLAGS) memory.o identity.o -o memory

memory.o: memory.cpp 
	$(CPP) $(CPPFLAGS) -c -o memory.o memory.cpp

identity.o: identity.cpp
	$(CPP) $(CPPFLAGS) -c -o identity.o identity.cpp

# Memory V2
memoryV2: memoryV2.o identity.o papi_util.o papi_counters.o
	$(CPP) $(CPPFLAGS) $(MEMORYV2_FLAGS) memoryV2.o identity.o

memoryV2.o: memory.cpp
	$(CPP) $(CPPFLAGS) $(MEMORYV2_FLAGS) -c -o memoryV2.o memory.cpp

# Papi
papi_util.o: papi_util.c papi_util.h
	$(CC) $(CFLAGS) $(PAPI_FLAGS) -c -o papi_util.o papi_util.c

papi_counters.o: papi_counters.c papi_util.h
	$(CC) $(CFLAGS) $(PAPI_FLAGS) -c -o papi_counters.o papi_counters.c

clean:
	rm *.o
	rm -f stream
	rm -f stream_interfere
	rm -f streamV2
	rm -f streamV2_interfere
	rm -f metadata
	rm -f memory
	rm -f memoryV2



