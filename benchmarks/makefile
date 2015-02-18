

all: copy

.PHONY: copy
copy: build
	mkdir -p bin
	cd stream/src && cp stream ../../bin/stream
	cd stream/src && cp stream_interfere ../../bin/stream_interfere
	cd iobench && cp iobench.jar ../bin/iobench.jar
	cd job/bin && cp example ../../bin/memory
	cd metadata && cp src/metadata ../bin/metadata

.PHONY: build
build:
	cd stream && make
	cd iobench && make
	cd job && make
	cd metadata/src && make

clean:
	cd stream && make clean
	cd iobench && make clean
	cd job && make clean
	cd metadata/src && make clean
	rm -rf bin/*
