

all: copy

.PHONY: build
build:
	cd hog && make
	cd alloctest && make
	cd filetest && make 
	cd marc && make
	cd SparseLib++/1.7 && make

.PHONY: copy
copy: build
	cp SparseLib++/1.7/testing/{td,tsp} bin
	cp SparseLib++/1.7/testing/*.txt bin
	cp marc/example bin
	cp alloctest/alloctest bin
	cp filetest/filetest bin
	cp hog/hog bin

clean:
	rm bin/*
	cd hog && make clean
	cd alloctest && make clean
	cd filetest && make clean
	cd marc && make clean
	cd SparseLib++/1.7 && make clean

