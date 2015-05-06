all: copy

.PHONY: build
build:
	cd src/hog && $(MAKE)
	cd src/alloctest && $(MAKE)
	cd src/filetest && $(MAKE)
	cd src/marc && $(MAKE)
	cd src/SparseLib++/1.7 && $(MAKE) all

.PHONY: copy
copy: build
	mkdir -p bin
	cp src/SparseLib++/1.7/testing/*.txt bin
	mv src/SparseLib++/1.7/testing/tsp bin
	mv src/SparseLib++/1.7/testing/td bin
	mv src/marc/example bin
	mv src/marc/exampleV2 bin
	mv src/alloctest/alloctest bin
	mv src/filetest/filetest bin
	mv src/hog/hog bin

clean:
	rm -f bin/*
	cd src/hog && make clean
	cd src/alloctest && make clean
	cd src/filetest && make clean
	cd src/marc && make clean
	cd src/SparseLib++/1.7 && make clean

