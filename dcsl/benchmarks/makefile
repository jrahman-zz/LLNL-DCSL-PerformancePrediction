

all: copy

.PHONY: copy
copy: build
	mkdir -p bin
	cd src && cp stream ../bin/stream
	cd src && cp streamV2 ../bin/streamV2
	cd src && cp stream_interfere ../bin/stream_interfere
	cd src && cp streamV2_interfere ../bin/streamV2_interfere
	cd iobench && cp iobench.jar ../bin/iobench.jar
	cd src && cp memory ../bin/memory
	cd src && cp memory_interfere ../bin/memory_interfere
	cd src && cp memoryV2 ../bin/memoryV2
	cd src && cp memoryV2_interfere ../bin/memoryV2_interfere
	cd src && cp metadata ../bin/metadata
	cd src && cp whetstone ../bin/whetstone
	cd src && cp dhrystone ../bin/dhrystone
	cd src && cp lloops ../bin/lloops
	cd src && cp linpack ../bin/linpack

.PHONY: build
build:
	cd src && $(MAKE)
	cd iobench && $(MAKE)

clean:
	cd src && make clean
	cd iobench && make clean
	rm -rf bin/*
