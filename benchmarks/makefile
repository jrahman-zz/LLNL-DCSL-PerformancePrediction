

all: copy

.PHONY: copy
copy: build
	mkdir -p bin
	cd stream/src && cp stream ../../bin/stream
	cd stream/src && cp streamV2 ../../bin/streamV2
	cd stream/src && cp stream_interfere ../../bin/stream_interfere
	cd stream/src && cp streamV2_interfere ../../bin/streamV2_interfere
	cd iobench && cp iobench.jar ../bin/iobench.jar
	cd job/bin && cp example ../../bin/memory
	cd job/bin && cp exampleV2 ../../bin/memoryV2
	cd job/bin && cp alloctest ../../bin/alloctest
	cd metadata && cp src/metadata ../bin/metadata

.PHONY: build
build:
	cd stream && $(MAKE)
	cd iobench && $(MAKE)
	cd job && $(MAKE)
	cd metadata/src && $(MAKE)

clean:
	cd stream && make clean
	cd iobench && make clean
	cd job && make clean
	cd metadata/src && make clean
	rm -rf bin/*
