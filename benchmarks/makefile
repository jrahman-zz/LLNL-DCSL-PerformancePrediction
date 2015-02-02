

all: copy

.PHONY: copy
copy: build
	mkdir -p bin/stream
	cd stream/src && cp stream stream_interfere ../../bin/stream
	mkdir -p bin/iobench
	cd iobench && cp iobench.jar ../bin/iobench

.PHONY: build
build:
	cd stream && make
	cd iobench && make

clean:
	cd stream && make clean
	cd iobench && make clean
	rm -rf bin/stream/*
	rm -rf bin/iobench/*
