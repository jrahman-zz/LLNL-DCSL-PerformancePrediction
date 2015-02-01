all: copy

.PHONY: build
build:
	cd hog && make
	cd alloctest && make
	cd filetest && make 
	cd marc && make
	cd SparseLib++/1.7 && make all

.PHONY: copy
copy: build
	cp SparseLib++/1.7/testing/*.txt bin
	cp SparseLib++/1.7/testing/tsp bin
	cp SparseLib++/1.7/testing/td bin
	cp marc/example bin
	cp alloctest/alloctest bin
	cp filetest/filetest bin
	cp hog/hog bin

clean:
	rm -f bin/*
	cd hog && make clean
	cd alloctest && make clean
	cd filetest && make clean
	cd marc && make clean
	cd SparseLib++/1.7 && make clean

