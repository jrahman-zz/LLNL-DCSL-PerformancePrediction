

all: build

build: metadata

metadata: metadata.cpp
	g++ metadata.cpp -lrt -o metadata

.PHONY: clean
clean:
	rm metadata
