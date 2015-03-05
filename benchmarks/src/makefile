CC = gcc
CPP = g++

PAPI_PATH=/usr/lib/x86_64-linux-gnu/

COMMON = -L$(PAPI_PATH)/libpapi.so -l:libpapi.so

CFLAGS = -Wall
CPPFLAGS = -Wall -std=c++11

PAPI_OBJS = papi_util.o papi_counters.o

STREAM_FLAGS = -O2 $(COMMON)
STREAMV2_FLAGS = -O0 $(COMMON)
METADATA_FLAGS = -lrt $(COMMON)
MEMORY_FLAGS = -lrt -$(COMMON)
MEMORYV2_FLAGS = -lrt -DV2 -DREGULAR_STRIDE=1024 -DRANDOM_STRIDE=512 -DBANDWIDTH_SCALE=100000 $(COMMON)
PAPI_FLAGS = -std=c99 $(COMMON)

all: build

build: benchmarks interference

.PHONY: benchmarks
benchmarks: stream streamV2 metadata memory memoryV2

.PHONY: interference
interference: stream_interfere streamV2_interfere metadata_interfere memory_interfere memoryV2_interfere

# Stream
stream: stream.c $(PAPI_OBJS)
	$(CC) $(CFLAGS) $(STREAM_FLAGS) stream.c $(PAPI_OBJS) -o stream

stream_interfere: stream.c
	$(CC) $(CFLAGS) $(STREAM_FLAGS) -DINTERFERE stream.c -o stream_interfere

# Stream V2
streamV2: stream.c $(PAPI_OBJS)
	$(CC) $(CFLAGS) $(STREAMV2_FLAGS) stream.c $(PAPI_OBJS) -DNTIMES=100000 -o streamV2

streamV2_interfere: stream.c
	$(CC) $(CFLAGS) $(STREAMV2_FLAGS) stream.c -DINTERFERE -DNTIMES=100000 -o streamV2_interfere

# Metadata
metadata: metadata.cpp
	$(CPP) $(CPPFLAGS) metadata.cpp $(METADATA_FLAGS) -o metadata

metadata_interfere: metadata.cpp
	$(CPP) $(CPPFLAGS) metadata.cpp -DINTERFERE -o metadata_intefere

# Memory
memory: memory.o identity.o $(PAPI_OBJS)
	$(CPP) $(CPPFLAGS) $(MEMORY_FLAGS) memory.o identity.o $(PAPI_OBJS) -o memory

memory_interfere: memory_interfere.o identity.o
	$(CPP) $(CPPFLAGS) $(MEMORY_FLAGS) memory_interfere.o identity.o -o memory_interfere

memory.o: memory.cpp 
	$(CPP) $(CPPFLAGS) $(MEMORY_FLAGS) -c -o memory.o memory.cpp

memory_interfere.o: memory.cpp
	$(CPP) $(CPPFLAGS) $(MEMORY_FLAGS) -DINTERFERE -c -o memory_interfere memory.cpp

identity.o: identity.cpp
	$(CPP) $(CPPFLAGS) -c -o identity.o identity.cpp

# Memory V2
memoryV2: memoryV2.o identity.o $(PAPI_OBJS)
	$(CPP) $(CPPFLAGS) $(MEMORYV2_FLAGS) memoryV2.o identity.o $(PAPI_OBJS) -o memoryV2

memoryV2_interfere: memoryV2_interfere.o identity.o
	$(CPP) $(CPPFLAGS) $(MEMORYV2_FALGS) memoryV2_interfere.o identity.o -o memoryV2_interfere

memoryV2.o: memory.cpp
	$(CPP) $(CPPFLAGS) $(MEMORYV2_FLAGS) -c -o memoryV2.o memory.cpp

memoryV2_interfere.o: memory.cpp
	$(CPP) $(CPPFLAGS) $(MEMORYV2_FLAGS) -c -o memoryV2_interfere.o memory.cpp

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



