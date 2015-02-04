

all: copy

.PHONY: copy
copy: build
	mkdir -p bin/stream
	cd stream/src && cp stream stream_interfere ../../bin/stream
	mkdir -p bin/iobench
	cd iobench && cp iobench.jar ../bin/iobench
	mkdir -p bin/memory
	cd job/bin && cp example ../../bin/memory

.PHONY: build
build:
	cd stream && make
	cd iobench && make
	cd job && make

clean:
	cd stream && make clean
	cd iobench && make clean
	cd job && make clean
	rm -rf bin/stream/*
	rm -rf bin/iobench/*
	rm -rf bin/memory/*
